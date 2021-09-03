import logging
from functools import reduce
from itertools import accumulate
from operator import mul

from dune.codegen.blockstructured.geometry import compute_multilinear_to_global_transformation, \
    compute_axiparallel_to_global_transformation
from dune.codegen.blockstructured.tools import sub_element_inames
from dune.codegen.cgen.clazz import ClassMember
from dune.codegen.error import CodegenError
from dune.codegen.generation import delete_cache_items, run_hook, ReturnArg, global_context, instruction, globalarg, \
    geometry_mixin, temporary_variable, get_global_context_value, class_member, include_file, domain, \
    generator_factory, iname, initializer_list, quadrature_mixin, get_counted_variable
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.options import get_form_option, form_option_context, get_option
from dune.codegen.pdelab.geometry import world_dimension, GenericPDELabGeometryMixin
from dune.codegen.pdelab.localoperator import extract_kernel_from_cache, get_visitor, \
    generate_localoperator_file, local_operator_default_settings, generate_residual_kernels, generate_jacobian_kernels, \
    enum_pattern, pattern_baseclass, enum_alpha, lop_template_ansatz_gfs, name_ansatz_gfs_constructor_param
import pymbolic.primitives as prim
from dune.codegen.pdelab.quadrature import GenericQuadratureMixin
from dune.codegen.tools import get_pymbolic_basename
from loopy.match import Writes
from ufl import replace, Form
from ufl.classes import Expr
import loopy as lp


def generate_preconditioner_files(form, original_form):
    logger = logging.getLogger(__name__)

    cmake_target = get_option("target_name")
    operator = get_global_context_value("form_identifier")

    def to_pdelab_mixin(s):
        return "generic" if s == "multilinear" else s

    coarse_form = transform(form)
    coarse_original_form = transform(original_form)

    logger.info("{}: create local operator for coarse grid".format(__name__))
    delete_cache_items()
    with form_option_context(blockstructured=False, classname='{}CoarseOperator'.format(operator),
                             generate_jacobians=True, generate_jacobian_apply=False,
                             blockstructured_preconditioner=None, matrix_free=False,
                             geometry_mixins=to_pdelab_mixin(get_form_option("geometry_mixins").split("_")[-1]),
                             quadrature_mixins="generic", basis_mixins="generic", accumulation_mixins="generic"):
        data = get_global_context_value("data")
        data.object_by_name[get_form_option("form")] = coarse_original_form
        local_operator_default_settings(operator, form)
        kernel_dict = {}
        kernel_dict.update(generate_residual_kernels(coarse_form, coarse_original_form))
        kernel_dict.update(generate_jacobian_kernels(coarse_form, coarse_original_form))
        generate_localoperator_file(kernel_dict, "{}_{}CoarseOperator_file.hh".format(cmake_target, operator))

        data.object_by_name[get_form_option("form")] = original_form

    fine_elements = set(arg.ufl_element() for arg in form.arguments())
    coarse_elements = set(arg.ufl_element() for arg in coarse_form.arguments())
    if len(fine_elements) > 1 or len(coarse_elements) > 1:
        raise CodegenError("Preconditioner does not support different finite elements")
    else:
        fine_element, = fine_elements
        coarse_element, = coarse_elements

    if get_form_option("blockstructured_preconditioner") in ["neumann", "nn"]:
        logger.info("{}: create local decomposition for Neumann-Neumann preconditioner".format(__name__))
        delete_cache_items()
        with form_option_context(classname='LocalDecompositionOperator'):
            local_operator_default_settings(operator, form)
            generate_localoperator_file({("cell", "residual"): generate_local_decomposition(fine_element)},
                                        '{}_local_decomposition_operator_file.hh'.format(cmake_target))

    logger.info("{}: create interpolation local operator".format(__name__))
    delete_cache_items()
    with form_option_context(classname='InterpolationLocalOperator'):
        local_operator_default_settings(operator, form)
        generate_localoperator_file({("cell", "residual"): generate_interpolation(fine_element, coarse_element)},
                                    '{}_interpolation_operator_file.hh'.format(cmake_target))

    logger.info("{}: create restriction local operator".format(__name__))
    delete_cache_items()
    with form_option_context(classname='RestrictionLocalOperator'):
            local_operator_default_settings(operator, form)
            generate_localoperator_file({("cell", "residual"): generate_restriction(fine_element, coarse_element)},
                                        '{}_restriction_operator_file.hh'.format(cmake_target))

    if get_form_option("blockstructured_preconditioner") == "jacobi":
        logger.info("{}: create point diagonal local operator for Jacobi preconditioner".format(__name__))
        delete_cache_items()
        with form_option_context(classname="rPointDiagonal", blockstructured_preconditioner=None):
            from ufl import derivative
            from ufl.algorithms import replace
            from dune.codegen.ufl.preprocess import preprocess_form

            jacform = derivative(original_form, original_form.coefficients()[0])
            jacform = preprocess_form(jacform).preprocessed_form
            args = jacform.arguments()
            jacform = replace(jacform, {args[1]: args[0]})

            local_operator_default_settings(operator, jacform)
            kernel_dict = {}
            kernel_dict.update(generate_residual_kernels(jacform, original_form))
            generate_localoperator_file(kernel_dict, "{}_{}PointDiagonal_file.hh".format(cmake_target, operator))

    delete_cache_items()
    local_operator_default_settings(operator, form)


def transform(form):
    coarse_space = get_global_context_value("data").object_by_name.get("coarse_space")
    if coarse_space is None:
        return form
    else:
        mapping = {}
        for argument in form.arguments():
            mapping[argument] = type(argument)(coarse_space, argument.number(), argument.part())
        for coefficient in form.coefficients():
            mapping[coefficient] = type(coefficient)(coarse_space, coefficient.count())
        form = replace(form, mapping)

        integrals = []
        for integral in form.integrals():
            metadata = integral.metadata().copy()
            if "estimated_polynomial_degree" in metadata:
                del metadata["estimated_polynomial_degree"]
            integrals.append(integral.reconstruct(metadata=metadata))

        return Form(integrals)


def add_patterns():
    enum_pattern()
    pattern_baseclass()
    enum_alpha()


@generator_factory(item_tags=("domain",), context_tags="kernel")
def domain_with_bounds(iname, bounds):
    assert isinstance(bounds, (list, tuple))
    assert len(bounds) == 2
    return "{{ [{0}] : {1}<={0}<{2} }}".format(iname, *bounds)


@iname
def register_inames(names):
    return names


@class_member(classtag="operator")
def define_gridview_member(name):
    gfs_type = lop_template_ansatz_gfs()
    gfs_name = name_ansatz_gfs_constructor_param()
    initializer_list(name, ["{}.gridView()".format(gfs_name)], classtag="operator")

    return "const typename {}::Traits::GridView& {};".format(gfs_type, name)


def name_gridview_member():
    name = "_gv"
    define_gridview_member(name)
    return name


def extract_component(element, component):
    return element if element.value_shape() == () else element.extract_component(component)[1]


class LocalData(object):
    shape_ = dict()
    inames_ = dict()

    def __init__(self, name, element, blocks):
        self.data_name = name
        self.element = element
        self.blocks = blocks

        dim = element.cell().geometric_dimension()
        for component in range(element.value_size()):
            el = extract_component(element, component)
            self.shape_[(el, blocks)] = (el.degree() * blocks + 1,) * dim
            self.inames_[(el, blocks)] = tuple(get_counted_variable("i") for _ in range(dim))

    def base_init(self):
        base_name = "{}_base".format(self.data_name)
        globalarg(base_name, shape=())
        instruction(code="auto* {} = Dune::PDELab::accessBaseContainer({}).data();".format(base_name, self.data_name),
                    assignees=(base_name,))
        return base_name

    def components(self):
        return self.element.value_size()

    def name(self, component):
        base_name = self.base_init()
        name = self.data_name + str(component)
        offset = sum(reduce(mul, self.shape(i)) for i in range(component))
        globalarg(name, shape=self.shape(component), order='F')
        instruction(code="auto* {} = {} + {};".format(name, base_name, offset), assignees=(),
                    depends_on=frozenset({Writes(base_name)}))
        return name

    def shape(self, component):
        return self.shape_[(extract_component(self.element, component), self.blocks)]

    def inames(self, component, codim=0, subentity=0):
        element = extract_component(self.element, component)
        if codim == 0:
            domain(self.inames_[(element, self.blocks)], self.shape(component))
        elif codim == 1:
            facemod = subentity % 2
            facedir = subentity // 2

            for i, (name, shape) in enumerate(zip(self.inames_[(element, self.blocks)], self.shape(component))):
                if i != facedir:
                    domain(name, shape)
                else:
                    bounds = (facemod * (shape - 1), facemod * (shape - 1) + 1)
                    domain_with_bounds(name, bounds)
        else:
            raise NotImplementedError()
        return self.inames_[(element, self.blocks)]

    def interior_pred(self, component):
        interior_pred = []
        for iname, shape in zip(self.inames(component), self.shape(component)):
            interior_pred.append(prim.Comparison(prim.Variable(iname), '>', 0))
            interior_pred.append(prim.Comparison(prim.Variable(iname), '<', shape - 1))
        return prim.LogicalAnd(tuple(interior_pred))

    def exterior_pred(self, component):
        exterior_pred = []
        for iname, shape in zip(self.inames(component), self.shape(component)):
            exterior_pred.append(prim.Comparison(prim.Variable(iname), '==', 0))
            exterior_pred.append(prim.Comparison(prim.Variable(iname), '==', shape - 1))
        return prim.LogicalOr(tuple(exterior_pred))

    def __str__(self):
        return self.data_name


@class_member(classtag="operator")
def define_local_basis_eval(name, element):
    basis_size = (element.degree() + 1) ** world_dimension()
    rf = type_floatingpoint()
    globalarg(name, shape=(basis_size, 1), managed=False)
    return "mutable std::vector<Dune::FieldVector<{}, 1>> {} = " \
           "std::vector<Dune::FieldVector<{}, 1>>({});".format(rf, name, rf, basis_size)


def name_coarse_basis_eval(element):
    name = 'phi{}{}'.format(element._short_name, element.degree())
    define_local_basis_eval(name, element)
    return name


@class_member(classtag="operator")
def define_local_basis(name, element):
    rf = type_floatingpoint()
    include_file("dune/localfunctions/lagrange/lagrangecube.hh", filetag='operatorfile')
    basis_type = "Dune::Impl::LagrangeCubeLocalBasis<{}, {}, {}, {}>".format(rf, rf, world_dimension(), element.degree())
    return "{} {};".format(basis_type, name)


def name_coarse_basis(element):
    name = 'coarseBasis{}{}'.format(element._short_name, element.degree())
    define_local_basis(name, element)
    return name


def evaluate_coarse_basis(point, element, within_inames):
    eval_name = name_coarse_basis_eval(element)
    basis = name_coarse_basis(element)

    instruction(code="{}.evaluateFunction({}, {});".format(basis, point, eval_name),
                assignees=(eval_name,),
                within_inames=frozenset(within_inames),
                depends_on=frozenset({Writes(point), Writes(eval_name)})
                )


def pymbolic_dof(element, inames):
    name = 'dof{}{}'.format(element._short_name, element.degree())

    dim = world_dimension()
    temporary_variable(name, shape=(dim,), shape_impl=("fv",))

    dofs_1d = get_form_option("number_of_blocks") * element.degree()
    for i, iname in enumerate(inames):
        instruction(assignee=prim.Subscript(prim.Variable(name), (i,)),
                    expression=prim.Variable(iname) / dofs_1d,
                    within_inames=frozenset(inames))
    return prim.Variable(name)


@quadrature_mixin("local_decomposition")
class LocalDecompositionQuadratureMixin(GenericQuadratureMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quad_inames = kwargs["inames"]

    def quadrature_inames(self):
        return self.quad_inames


@geometry_mixin("local_decomposition_multilinear")
class LocalDecompositionGeometryMixin(GenericPDELabGeometryMixin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.element = kwargs["element"]

    def spatial_coordinate(self, o):
        local = pymbolic_dof(self.element, self.quadrature_inames())
        assert isinstance(local, prim.Expression)
        name = get_pymbolic_basename(local) + "_global"

        # TODO need to assert somehow that local is of codim 0
        compute_multilinear_to_global_transformation(name, local, self)
        return prim.Variable(name)


@geometry_mixin("local_decomposition_axiparallel")
class LocalDecompositionGeometryAPMixin(LocalDecompositionGeometryMixin):
    def spatial_coordinate(self, o):
        local = pymbolic_dof(self.element, self.quadrature_inames())
        assert isinstance(local, prim.Expression)
        name = get_pymbolic_basename(local) + "_global"

        # TODO need to assert somehow that local is of codim 0
        compute_axiparallel_to_global_transformation(name, local, self)
        return prim.Variable(name)


@geometry_mixin("local_decomposition_equidistant")
class LocalDecompositionGeometryEQMixin(LocalDecompositionGeometryAPMixin):
    pass


def generate_local_decomposition(finite_element):
    dofs_1d = get_form_option("number_of_blocks")

    def get_dirichlet_pred(element, component_index, inames):
        # TODO: get the dirichlet condition without so many assumptions
        # TODO: this is a function call to add temporary variables to the loopy kernel
        dirichlet_pred_ufl = get_global_context_value("data").object_by_name.get('is_dirichlet')
        if isinstance(dirichlet_pred_ufl, tuple):
            dirichlet_pred_ufl = dirichlet_pred_ufl[component_index]
        if isinstance(dirichlet_pred_ufl, Expr):
            # condition is an ufl expression -> transform
            with global_context(integral_type="cell"):
                with form_option_context(geometry_mixins="local_decomposition_" +
                                                         get_form_option("geometry_mixins").split("_")[-1],
                                         quadrature_mixins="local_decomposition"):
                    visitor = get_visitor('cell', 'otherwise', inames=inames, element=element)
                    dirichlet_pred = visitor(dirichlet_pred_ufl, do_predicates=True)
                    dirichlet_pred = prim.Comparison(dirichlet_pred, '==', 1)  # assume subdomain_id 1 is dirichlet
        else:
            # otherwise assume dirichlet_pred_ufl can be used as boolean expression
            dirichlet_pred = dirichlet_pred_ufl
        return dirichlet_pred

    def pymbolic_local_data(local, c, codim=0, subentity=0):
        return prim.Subscript(prim.Variable(local.name(c)), tuple(prim.Variable(i)
                                                                  for i in local.inames(c, codim, subentity)))

    def copy_cell(x, y):
        instruction(assignee=pymbolic_local_data(y, component_index),
                    expression=pymbolic_local_data(x, component_index),
                    within_inames=frozenset(x.inames(component_index)),
                    predicates=frozenset({x.interior_pred(component_index)}),
                    )

    # TODO: unclear, if neumann bc faces should also be copied
    def copy_interface(x, y):
        instruction(assignee=pymbolic_local_data(y, component_index),
                    expression=pymbolic_local_data(x, component_index),
                    within_inames=frozenset(x.inames(component_index)),
                    predicates=frozenset({x.exterior_pred(component_index)}),
                    )

    def copy_exterior_boundary_faceid(x, y, faceid):
        pred = get_dirichlet_pred(extract_component(x.element, component_index), component_index,
                                  x.inames(component_index, codim=1, subentity=faceid))
        instruction(assignee=pymbolic_local_data(y, component_index, codim=1, subentity=faceid),
                    expression=pymbolic_local_data(x, component_index, codim=1, subentity=faceid),
                    within_inames=frozenset(x.inames(component_index, codim=1, subentity=faceid)),
                    predicates=frozenset({pred}),
                    depends_on=frozenset({Writes(get_pymbolic_basename(d)) for d in
                                          lp.symbolic.DependencyMapper()(pred)})
                    )

    def signature(name):
        return ["template <typename EG, typename X, typename Y>",
                "void {}(const EG& eg, const X& x, Y& y) const".format(name)]

    delete_cache_items("kernel_default")
    kernels = []
    for generator in [copy_cell, copy_interface]:
        x = LocalData("x", finite_element, dofs_1d)
        y = LocalData("y", finite_element, dofs_1d)
        for component_index in range(finite_element.value_size()):
            generator(x, y)

        name = generator.__name__

        kernels.append(extract_kernel_from_cache("kernel_default", name, signature(name)))
        delete_cache_items("kernel_default")

    def copy_exterior_boundary_switch():
            block = """{
      if (eg.entity().hasBoundaryIntersections()) {
        for (const auto is: intersections(_gv, eg.entity())) {
          if (is.boundary()) {
            switch (is.indexInInside()) {
            }
          }
        }
      }
    }""".splitlines(keepends=False)
            cases = []
            for faceid in range(2 ** world_dimension()):
                cases.append("          case {0}: copy_exterior_boundary_faceid{0}(eg, x, y); break;".format(faceid))
            block = block[:len(block) // 2] + cases + block[len(block) // 2:]
            return block

    name_gridview_member()
    kernels.append(ClassMember(signature("copy_exterior_boundary") + copy_exterior_boundary_switch()))
    for faceid in range(2**world_dimension()):
        x = LocalData("x", finite_element, dofs_1d)
        y = LocalData("y", finite_element, dofs_1d)
        for component_index in range(finite_element.value_size()):
            copy_exterior_boundary_faceid(x, y, faceid)

        name = "copy_exterior_boundary_faceid{}".format(faceid)

        kernels.append(extract_kernel_from_cache("kernel_default", name, signature(name)))
        delete_cache_items("kernel_default")

    return kernels


def generate_grid_transfer(src, dst, src_is_fine):
    data_fine = src if src_is_fine else dst
    data_coarse = dst if src_is_fine else src
    with global_context(integral_type="cell", form_type="residual"):
        for component in range(src.components()):
            point = pymbolic_dof(extract_component(data_fine.element, component), data_fine.inames(component))
            eval_name = name_coarse_basis_eval(extract_component(data_coarse.element, component))
            evaluate_coarse_basis(point.name, element=extract_component(data_coarse.element, component),
                                  within_inames=data_fine.inames(component))

            flat_index = sum(prim.Variable(iname) * stride for iname, stride in
                             zip(data_coarse.inames(component), accumulate((1,) + data_coarse.shape(component)[:-1], mul)))

            assignee = prim.Subscript(prim.Variable(dst.name(component)),
                                      tuple(prim.Variable(i) for i in dst.inames(component)))
            instruction(assignee=assignee,
                        expression=(prim.Subscript(prim.Variable(eval_name), (flat_index, 0,)) *
                                    prim.Subscript(prim.Variable(src.name(component)),
                                                   tuple(prim.Variable(i) for i in src.inames(component))) +
                                    assignee),
                        within_inames=frozenset(dst.inames(component) + src.inames(component)),
                        depends_on=frozenset({Writes(eval_name)}))

        from dune.codegen.pdelab.signatures import kernel_name, assembly_routine_signature
        name = kernel_name()
        signature = assembly_routine_signature()
        knl = extract_kernel_from_cache("kernel_default", name, signature)
        delete_cache_items("kernel_default")

        # Run preprocessing from custom user code
        knl = run_hook(name="domain_count",
                       args=(ReturnArg(knl),),
                       )

        add_patterns()

    return [knl]


def generate_interpolation(finite_element, coarse_element):
    x = LocalData("x", coarse_element, 1)
    r = LocalData("r", finite_element, get_form_option("number_of_blocks"))
    return generate_grid_transfer(x, r, src_is_fine=False)


def generate_restriction(fine_element, coarse_element):
    x = LocalData("x", fine_element, get_form_option("number_of_blocks"))
    r = LocalData("r", coarse_element, 1)
    return generate_grid_transfer(x, r, src_is_fine=True)
