""" Generators for basis evaluations """

from dune.codegen.generation import (basis_mixin,
                                     class_member,
                                     include_file,
                                     instruction,
                                     kernel_cached,
                                     preamble,
                                     temporary_variable,
                                     )
from dune.codegen.options import get_form_option
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.pdelab.argument import (name_applycontainer,
                                          name_coefficientcontainer,
                                          )
from dune.codegen.pdelab.spaces import (lfs_iname,
                                        lfs_inames,
                                        name_leaf_lfs,
                                        name_lfs,
                                        name_lfs_bound,
                                        type_leaf_gfs,
                                        initialize_function_spaces,
                                        )
from dune.codegen.pdelab.geometry import (component_iname,
                                          world_dimension,
                                          )
from dune.codegen.pdelab.localoperator import (lop_template_ansatz_gfs,
                                               lop_template_test_gfs,
                                               name_coefficient_vector,
                                               name_coefficient_lfs,
                                               name_coefficient_lfs_cache,
                                               type_coefficient_vector,
                                               type_coefficient_lfs_cache,
                                               )
from dune.codegen.tools import (get_pymbolic_basename,
                                get_pymbolic_indices,
                                )
from dune.codegen.pdelab.driver import FEM_name_mangling
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.pdelab.driver import (isPk,
                                        isQk,
                                        isDG)
from dune.codegen.ufl.modified_terminals import Restriction

from pymbolic.primitives import Product, Subscript, Variable
import pymbolic.primitives as prim

from ufl import MixedElement

from loopy import Reduction


@basis_mixin("base")
class BasisMixinBase(object):
    def initialize_function_spaces(self, expr):
        pass

    def lfs_inames(self, element, restriction, number):
        raise NotImplementedError("Basis Mixins should implement local function space inames")

    def implement_basis(self, element, restriction, number):
        raise NotImplementedError("Basis Mixins should implement the basis")

    def implement_reference_gradient(self, element, restriction, number, index):
        raise NotImplementedError("Basis Mixins should implement the basis gradient")

    def implement_trialfunction(self, element, restriction, index):
        raise NotImplementedError("Basis Mixins should implement trial function evaluation")

    def implement_trialfunction_gradient(self, element, restriction, index):
        raise NotImplementedError("Basis Mixins should implement trial function gradient evaluation")

    def implement_apply_function(self, element, restriction, index):
        raise NotImplementedError("Basis Mixins should implement linearization point evaluation")

    def implement_apply_function_gradient(self, element, restriction, index):
        raise NotImplementedError("Basis Mixins should implement linearization point gradient evaluation")

    def implement_coefficient_function(self, coeff, restriction, index):
        raise NotImplementedError("Basis Mixins should implement grid function evaluation")

    def implement_coefficient_function_gradient(self, coeff, restriction, index):
        raise NotImplementedError("Basis Mixins should implement grid function evaluation")


@basis_mixin("generic")
class GenericBasisMixin(BasisMixinBase):
    def initialize_function_spaces(self, expr):
        restriction = self.restriction
        if self.measure == 'exterior_facet':
            restriction = Restriction.POSITIVE

        return initialize_function_spaces(expr, restriction, self.indices)

    def lfs_inames(self, element, restriction, number, context=""):
        return (lfs_iname(element, restriction, number, context),)

    def implement_basis(self, element, restriction, number, context=""):
        assert not isinstance(element, MixedElement)
        name = "phi_{}".format(FEM_name_mangling(element))
        name = restricted_name(name, restriction)
        self.evaluate_basis(element, name, restriction)
        iname, = self.lfs_inames(element, restriction, number, context=context)

        return prim.Subscript(prim.Variable(name), (prim.Variable(iname), 0))

    @kernel_cached
    def evaluate_basis(self, element, name, restriction):
        lfs_name = name_leaf_lfs(element, restriction)
        temporary_variable(name,
                           shape=(name_lfs_bound(lfs_name), 1),
                           decl_method=declare_cache_temporary(element, restriction, 'Function'),
                           )
        cache = name_localbasis_cache(element)
        qp = self.to_cell(self.quadrature_position())
        instruction(inames=self.quadrature_inames(),
                    code='{} = {}.evaluateFunction({}, {}.finiteElement().localBasis());'.format(name,
                                                                                                 cache,
                                                                                                 str(qp),
                                                                                                 lfs_name,
                                                                                                 ),
                    assignees=frozenset({name}),
                    read_variables=frozenset({get_pymbolic_basename(qp)}),
                    )

    def implement_reference_gradient(self, element, restriction, number, context=""):
        assert not isinstance(element, MixedElement)
        name = "js_{}".format(FEM_name_mangling(element))
        name = restricted_name(name, restriction)
        self.evaluate_reference_gradient(element, name, restriction)
        iname, = self.lfs_inames(element, restriction, number, context=context)

        return prim.Subscript(prim.Variable(name), (prim.Variable(iname), 0))

    @kernel_cached
    def evaluate_reference_gradient(self, element, name, restriction):
        lfs_name = name_leaf_lfs(element, restriction)
        temporary_variable(name,
                           shape=(name_lfs_bound(lfs_name), 1, world_dimension()),
                           decl_method=declare_cache_temporary(element, restriction, 'Jacobian'),
                           )
        cache = name_localbasis_cache(element)
        qp = self.to_cell(self.quadrature_position())
        instruction(inames=self.quadrature_inames(),
                    code='{} = {}.evaluateJacobian({}, {}.finiteElement().localBasis());'.format(name,
                                                                                                 cache,
                                                                                                 str(qp),
                                                                                                 lfs_name,
                                                                                                 ),
                    assignees=frozenset({name}),
                    read_variables=frozenset({get_pymbolic_basename(qp)}),
                    )

    def implement_trialfunction(self, element, restriction, index):
        rawname = "u_{}".format(index)
        name = restricted_name(rawname, restriction)
        container = name_coefficientcontainer(restriction)
        self.evaluate_coefficient(element, name, container, restriction, index)
        return prim.Variable(name)

    def implement_trialfunction_gradient(self, element, restriction, index):
        rawname = "gradu_{}".format(index)
        name = restricted_name(rawname, restriction)
        container = name_coefficientcontainer(restriction)
        self.evaluate_coefficient_gradient(element, name, container, restriction, index)
        return prim.Variable(name)

    def implement_apply_function(self, element, restriction, index):
        rawname = "z_func_{}".format(index)
        name = restricted_name(rawname, restriction)
        container = name_applycontainer(restriction)
        self.evaluate_coefficient(element, name, container, restriction, index)
        return prim.Variable(name)

    def implement_apply_function_gradient(self, element, restriction, index):
        rawname = "gradz_func_{}".format(index)
        name = restricted_name(rawname, restriction)
        container = name_applycontainer(restriction)
        self.evaluate_coefficient_gradient(element, name, container, restriction, index)
        return prim.Variable(name)

    @kernel_cached
    def evaluate_coefficient(self, element, name, container, restriction, index):
        sub_element = element
        if isinstance(element, MixedElement):
            sub_element = element.extract_component(index)[1]
        from ufl import FiniteElement
        assert isinstance(sub_element, FiniteElement)

        temporary_variable(name, shape=(), managed=True)

        basis = self.implement_basis(sub_element, restriction, 0, context="trial")
        basisindex = get_pymbolic_indices(basis)[:-1]

        lfs_name = name_lfs(element, restriction, index)

        # TODO get rid ot this!
        if get_form_option("blockstructured"):
            from dune.codegen.blockstructured.argument import pymbolic_coefficient
            coeff = pymbolic_coefficient(container, lfs_name, sub_element, basisindex)
        else:
            from dune.codegen.pdelab.argument import pymbolic_coefficient
            coeff = pymbolic_coefficient(container, lfs_name, basisindex[0])

        assignee = prim.Variable(name)
        reduction_expr = prim.Product((coeff, basis))

        instruction(expression=Reduction("sum", basisindex, reduction_expr, allow_simultaneous=True),
                    assignee=assignee,
                    forced_iname_deps=frozenset(self.quadrature_inames()),
                    forced_iname_deps_is_final=True,
                    )

    @kernel_cached
    def evaluate_coefficient_gradient(self, element, name, container, restriction, index):
        sub_element = element
        if isinstance(element, MixedElement):
            sub_element = element.extract_component(index)[1]
        from ufl import FiniteElement
        assert isinstance(sub_element, FiniteElement)

        temporary_variable(name, shape=(element.cell().geometric_dimension(),), managed=True)

        dimindex = component_iname(count=0)

        basis = self.implement_reference_gradient(sub_element, restriction, 0, context='trialgrad')
        basisindex = get_pymbolic_indices(basis)[:-1]
        from dune.codegen.tools import maybe_wrap_subscript
        basis = maybe_wrap_subscript(basis, prim.Variable(dimindex))

        lfs_name = name_lfs(element, restriction, index)

        # TODO get rid of this
        if get_form_option("blockstructured"):
            from dune.codegen.blockstructured.argument import pymbolic_coefficient
            coeff = pymbolic_coefficient(container, lfs_name, sub_element, basisindex)
        else:
            from dune.codegen.pdelab.argument import pymbolic_coefficient
            coeff = pymbolic_coefficient(container, lfs_name, basisindex[0])

        assignee = prim.Subscript(prim.Variable(name), (prim.Variable(dimindex),))
        reduction_expr = prim.Product((coeff, basis))

        instruction(expression=Reduction("sum", basisindex, reduction_expr, allow_simultaneous=True),
                    assignee=assignee,
                    forced_iname_deps=frozenset(self.quadrature_inames()).union(frozenset({dimindex})),
                    forced_iname_deps_is_final=True,
                    )

    def _name_coefficient_container(self, coeff, restriction):
        # This will be the LocalVector object in the generated PDELab code that
        # contains the local coefficients.
        name = "local_coefficient_vector_{}".format(coeff.count())
        name = restricted_name(name, restriction)
        fill_coefficient_container(name, coeff, restriction)
        return name

    def implement_coefficient_function(self, coeff, restriction, index):
        rawname = "coefficientFunction{}_{}".format(coeff.count(), index)
        name = restricted_name(rawname, restriction)
        container = self._name_coefficient_container(coeff, restriction)
        self.evaluate_coefficient(coeff.ufl_element(), name, container, restriction, index)
        return prim.Variable(name)

    def implement_coefficient_function_gradient(self, coeff, restriction, index):
        rawname = "coefficientFunctionGradient{}_{}".format(coeff.count(), index)
        name = restricted_name(rawname, restriction)
        container = self._name_coefficient_container(coeff, restriction)
        self.evaluate_coefficient_gradient(coeff.ufl_element(), name, container, restriction, index)
        return prim.Variable(name)


@preamble
def fill_coefficient_container(name, coeff, restriction):
    # Generate the code that fills the local coefficient vector with the
    # correct degrees of freedom
    coeff_name = name_coefficient_vector(coeff, restriction)
    coeff_type = type_coefficient_vector(coeff)
    lfs_name = name_coefficient_lfs(coeff, restriction)
    lfs_cache_name = name_coefficient_lfs_cache(coeff, restriction)
    lfs_cache_type = type_coefficient_lfs_cache(coeff)
    coeff_view = "coefficient_view_{}".format(coeff.count())
    coeff_iew = restricted_name(coeff_view, restriction)
    return ["typename {}::template LocalView<{}> {}(*{});".format(coeff_type,
                                                                  lfs_cache_type,
                                                                  coeff_view,
                                                                  coeff_name),
            "{}->update();".format(lfs_cache_name),
            "Dune::PDELab::LocalVector<{}> {}({}->size());".format(type_floatingpoint(), name, lfs_name),
            "{}.bind(*{});".format(coeff_view, lfs_cache_name),
            "{}.read({});".format(coeff_view, name),
            "{}.unbind();".format(coeff_view)]


def declare_grid_function_range(gridfunction):
    def _decl(name, kernel, decl_info):
        return "typename std::decay_t<decltype(*{})>::Range {};".format(gridfunction, name)

    return _decl


@class_member(classtag="operator")
def typedef_localbasis(element, name):
    basis_type = "{}::Traits::FiniteElementMap::Traits::FiniteElementType::Traits::LocalBasisType".format(type_leaf_gfs(element))
    return "using {} = typename {};".format(name, basis_type)


def type_localbasis(element):
    if isPk(element):
        name = "P{}_LocalBasis".format(element._degree)
    elif isQk(element):
        name = "Q{}_LocalBasis".format(element._degree)
    elif isDG(element):
        name = "DG{}_LocalBasis".format(element._degree)
    else:
        raise NotImplementedError("Element type not known in code generation")

    # TODO get rid of this
    if get_form_option("blockstructured"):
        from dune.codegen.blockstructured.basis import typedef_localbasis as bs_typedef_localbasis
        bs_typedef_localbasis(element, name)
    else:
        typedef_localbasis(element, name)

    return name


def type_localbasis_cache(element):
    return "LocalBasisCacheWithoutReferences<{}>".format(type_localbasis(element))


@class_member(classtag="operator")
def define_localbasis_cache(element, name):
    include_file("dune/codegen/localbasiscache.hh", filetag="operatorfile")
    t = type_localbasis_cache(element)
    return "{} {};".format(t, name)


def name_localbasis_cache(element):
    name = "cache_{}".format(FEM_name_mangling(element))
    define_localbasis_cache(element, name)
    return name


def declare_cache_temporary(element, restriction, which):
    t_cache = type_localbasis_cache(element)
    lfs = name_leaf_lfs(element, restriction)

    def decl(name, kernel, decl_info):
        return "typename {}::{}ReturnType {};".format(t_cache,
                                                      which,
                                                      name,
                                                      )
    return decl


def shape_as_pymbolic(shape):
    def _shape_as_pymbolic(s):
        if isinstance(s, str):
            return Variable(s)
        else:
            return s
    return tuple(_shape_as_pymbolic(s) for s in shape)
