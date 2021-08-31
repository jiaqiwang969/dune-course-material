from dune.codegen.blockstructured.geometry import name_face_id
from dune.codegen.blockstructured.quadrature import estimate_quadrature_bound
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.ufl.modified_terminals import Restriction
from loopy import Reduction

from dune.codegen.generation import (basis_mixin,
                                     kernel_cached,
                                     instruction,
                                     temporary_variable,
                                     globalarg,
                                     class_member,
                                     initializer_list,
                                     include_file, preamble)
from dune.codegen.tools import get_pymbolic_basename, get_pymbolic_indices
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.pdelab.basis import (GenericBasisMixin,
                                       type_localbasis,
                                       FEM_name_mangling)
from dune.codegen.pdelab.driver import (isPk,
                                        isQk,
                                        )
from dune.codegen.pdelab.geometry import world_dimension, component_iname, local_dimension
from dune.codegen.pdelab.spaces import type_leaf_gfs, name_lfs
from dune.codegen.blockstructured.spaces import lfs_inames
from dune.codegen.blockstructured.tools import tensor_index_to_sequential_index

from ufl import MixedElement

import pymbolic.primitives as prim


@basis_mixin("blockstructured")
class BlockStructuredBasisMixin(GenericBasisMixin):
    def lfs_inames(self, element, restriction, number, context=""):
        return lfs_inames(element, restriction, number, context=context)

    def _implement_reference_evaluation(self, which, element, restriction, number, context):
        assert not isinstance(element, MixedElement)

        evaluated_name = {"function": name_evaluated_basis,
                          "gradient": name_evaluated_gradient}

        qp = get_pymbolic_basename(self.quadrature_position_in_micro())
        name = evaluated_name[which](element, restriction, qp)
        inames = self.lfs_inames(element, restriction, number, context=context)
        offset = 0 if restriction == Restriction.NONE else estimate_quadrature_bound() * prim.Variable(
            name_face_id(restriction))

        return prim.Subscript(prim.Variable(name),
                              tuple(prim.Variable(q) + offset for q in self.quadrature_inames_in_micro()) +
                              (tensor_index_to_sequential_index(inames, element.degree() + 1), 0))

    def implement_basis(self, element, restriction, number, context=''):
        return self._implement_reference_evaluation("function", element, restriction, number, context)

    def implement_reference_gradient(self, element, restriction, number, context=''):
        return self._implement_reference_evaluation("gradient", element, restriction, number, context)

    @kernel_cached
    def evaluate_coefficient_gradient(self, element, name, container, restriction, index):
        sub_element = element
        if isinstance(element, MixedElement):
            sub_element = element.extract_component(index)[1]
        from ufl import FiniteElement
        assert isinstance(sub_element, FiniteElement)

        temporary_variable(name, shape=(element.cell().geometric_dimension(),), managed=True)

        dimindex = component_iname(count=0)

        lfs = name_lfs(element, restriction, index)
        basis = self.implement_reference_gradient(sub_element, restriction, 0, context='trialgrad')
        basisindex = get_pymbolic_indices(basis)[1:-1]
        from dune.codegen.tools import maybe_wrap_subscript
        basis = maybe_wrap_subscript(basis, prim.Variable(dimindex))

        from dune.codegen.blockstructured.argument import pymbolic_coefficient
        coeff = pymbolic_coefficient(container, lfs, sub_element, basisindex)

        assignee = prim.Subscript(prim.Variable(name), (prim.Variable(dimindex),))
        reduction_expr = prim.Product((coeff, basis))

        instruction(expression=Reduction("sum", basisindex, reduction_expr, allow_simultaneous=True),
                    assignee=assignee,
                    within_inames=frozenset(self.quadrature_inames() + (dimindex,)),
                    within_inames_is_final=True,
                    )

    @kernel_cached
    def evaluate_coefficient(self, element, name, container, restriction, index):
        sub_element = element
        if isinstance(element, MixedElement):
            sub_element = element.extract_component(index)[1]

        from ufl import FiniteElement
        assert isinstance(sub_element, FiniteElement)

        temporary_variable(name, shape=(), managed=True)

        lfs = name_lfs(element, restriction, index)
        basis = self.implement_basis(sub_element, restriction, 0, context='trial')
        basisindex = get_pymbolic_indices(basis)[1:-1]

        from dune.codegen.blockstructured.argument import pymbolic_coefficient
        coeff = pymbolic_coefficient(container, lfs, sub_element, basisindex)

        assignee = prim.Variable(name)
        reduction_expr = prim.Product((coeff, basis))

        instruction(expression=Reduction("sum", basisindex, reduction_expr, allow_simultaneous=True),
                    assignee=assignee,
                    within_inames=frozenset(self.quadrature_inames()),
                    within_inames_is_final=True,
                    )


# define FE basis explicitly in localoperator
@class_member(classtag="operator")
def typedef_localbasis(element, name):
    df = "typename {}::Traits::GridView::ctype".format(type_leaf_gfs(element))
    r = type_floatingpoint()
    dim = world_dimension()
    if isPk(element):
        include_file("dune/localfunctions/lagrange/lagrangesimplex.hh", filetag="operatorfile")
        basis_type = "Impl::LagrangeSimplexLocalBasis<{}, {}, {}, {}>".format(df, r, dim, element._degree)
    elif isQk(element):
        include_file("dune/localfunctions/lagrange/lagrangecube.hh", filetag="operatorfile")
        basis_type = "Impl::LagrangeCubeLocalBasis<{}, {}, {}, {}>".format(df, r, dim, element._degree)
    else:
        raise NotImplementedError("Element type not known in code generation")
    return "using {} = Dune::{};".format(name, basis_type)


@class_member(classtag="operator")
def define_localbasis(leaf_element, name):
    localBasis_type = type_localbasis(leaf_element)
    initializer_list(name, (), classtag="operator")
    return "const {} {};".format(localBasis_type, name)


def name_localbasis(leaf_element):
    name = "{}_microElementBasis".format(FEM_name_mangling(leaf_element))
    globalarg(name)
    define_localbasis(leaf_element, name)
    return name


@preamble(kernel='operator')
def init_evaluated_basis(name, element, qp, restriction, which):
    localbasis = name_localbasis(element)
    func = {"function": "evaluateFunction",
            "gradient": "evaluateJacobian"}
    if restriction == Restriction.NONE:
        return ["for (int i = 0; i < {}.size(); ++i)".format(qp),
                "{",
                "  {}.{}({}[i], {}[i]);".format(localbasis, func[which], qp, name),
                "}"]
    else:
        return ["for (int f_id = 0; f_id < {}; ++f_id)".format(2 * world_dimension()),
                "{",
                "  auto ref_el = Dune::referenceElement<{}, {}>(Dune::GeometryTypes::cube({}));".format(
                    type_floatingpoint(), world_dimension(), world_dimension()),
                "  auto is_geo = ref_el.geometry<1>(f_id);",
                "  for (int i = 0; i < {}.size(); ++i)".format(qp),
                "  {",
                "    auto qp_in_inside = is_geo.global({}[i]);".format(qp),
                "    {}.{}(qp_in_inside, {}[i + {} * f_id]);".format(localbasis, func[which], name,
                                                                     estimate_quadrature_bound()),
                "  }",
                "}"]


@class_member(classtag="operator")
def define_evaluated_basis(name, element, restriction, which):
    t_basis = type_localbasis(element)
    quadrature_bound = estimate_quadrature_bound() if restriction == Restriction.NONE \
        else estimate_quadrature_bound() * 2 * world_dimension()
    t_return = {"function": "RangeType",
                "gradient": "JacobianType"}
    return "std::array<std::vector<typename {}::Traits::{}>, {}> {};".format(t_basis, t_return[which],
                                                                             quadrature_bound, name)


def name_evaluated_basis(element, restriction, qp):
    name = "phi_{}".format(FEM_name_mangling(element))
    name = restricted_name(name, restriction)
    quadrature_bound = estimate_quadrature_bound() if restriction == Restriction.NONE \
        else estimate_quadrature_bound() * 2 * world_dimension()
    globalarg(name, shape=(quadrature_bound, (element.degree() + 1) ** world_dimension(), 1), managed=False)
    define_evaluated_basis(name, element, restriction, "function")
    init_evaluated_basis(name, element, qp, restriction, "function")
    return name


def name_evaluated_gradient(element, restriction, qp):
    name = "js_{}".format(FEM_name_mangling(element))
    name = restricted_name(name, restriction)
    quadrature_bound = estimate_quadrature_bound() if restriction == Restriction.NONE \
        else estimate_quadrature_bound() * 2 * world_dimension()
    globalarg(name, shape=(quadrature_bound, (element.degree() + 1) ** world_dimension(), 1, world_dimension()),
              managed=False)
    define_evaluated_basis(name, element, restriction, "gradient")
    init_evaluated_basis(name, element, qp, restriction, "gradient")
    return name
