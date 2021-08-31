from __future__ import absolute_import

import logging

import numpy as np

from dune.codegen.options import (get_form_option,
                                  get_option,
                                  form_option_context,
                                  )
from dune.codegen.generation import (accumulation_mixin,
                                     base_class,
                                     class_basename,
                                     class_member,
                                     construct_from_mixins,
                                     constructor_parameter,
                                     dump_accumulate_timer,
                                     register_liwkid_timer,
                                     end_of_file,
                                     generator_factory,
                                     get_global_context_value,
                                     global_context,
                                     include_file,
                                     initializer_list,
                                     kernel_cached,
                                     post_include,
                                     retrieve_cache_items,
                                     ReturnArg,
                                     run_hook,
                                     template_parameter,
                                     dump_ssc_marks
                                     )
from dune.codegen.cgen.clazz import ClassMember
from dune.codegen.pdelab.driver import is_linear
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.tools import get_pymbolic_basename
from dune.codegen.ufl.modified_terminals import Restriction
from frozendict import frozendict
from loopy.match import Writes

from pymbolic.primitives import Variable
import pymbolic.primitives as prim
from pytools import Record, ImmutableRecord

import loopy as lp
import cgen


@template_parameter(classtag="operator")
def lop_template_ansatz_gfs():
    name = "GFSU"
    constructor_parameter("const {}&".format(name), name_ansatz_gfs_constructor_param(), classtag="operator")
    return name


def name_ansatz_gfs_constructor_param():
    return "gfsu"


@template_parameter(classtag="operator")
def lop_template_test_gfs():
    name = "GFSV"
    constructor_parameter("const {}&".format(name), name_test_gfs_constructor_param(), classtag="operator")
    return name


def name_test_gfs_constructor_param():
    return "gfsv"


@class_member(classtag="operator")
def lop_domain_field(name):
    # TODO: Rethink for not Galerkin Method
    gfs = lop_template_ansatz_gfs()
    return "using {} = typename {}::Traits::GridView::ctype;".format(name, gfs)


def name_domain_field():
    name = "DF"
    lop_domain_field(name)
    return name


def name_initree_constructor_param():
    return "iniParams"


@class_member(classtag="operator")
def define_initree(name):
    param_name = name_initree_constructor_param()
    include_file('dune/common/parametertree.hh', filetag="operatorfile")
    constructor_parameter("const Dune::ParameterTree&", param_name, classtag="operator")
    initializer_list(name, [param_name], classtag="operator")

    return "const Dune::ParameterTree& {};".format(name)


@class_member(classtag="operator")
def _enum_pattern(which):
    return "enum {{ doPattern{} = true }};".format(which)


def enum_pattern():
    from dune.codegen.generation import get_global_context_value
    integral_type = get_global_context_value("integral_type")
    from dune.codegen.pdelab.signatures import ufl_measure_to_pdelab_measure
    return _enum_pattern(ufl_measure_to_pdelab_measure(integral_type))


def _pattern_baseclass(measure):
    return base_class('Dune::PDELab::Full{}Pattern'.format(measure), classtag="operator")


def pattern_baseclass():
    from dune.codegen.generation import get_global_context_value
    integral_type = get_global_context_value("integral_type")
    from dune.codegen.pdelab.signatures import ufl_measure_to_pdelab_measure
    return _pattern_baseclass(ufl_measure_to_pdelab_measure(integral_type))


@class_member(classtag="operator")
def _enum_alpha(which):
    return "enum {{ doAlpha{} = true }};".format(which)


def enum_alpha():
    from dune.codegen.generation import get_global_context_value
    integral_type = get_global_context_value("integral_type")
    from dune.codegen.pdelab.signatures import ufl_measure_to_pdelab_measure
    return _enum_alpha(ufl_measure_to_pdelab_measure(integral_type))


@class_member(classtag="operator")
def enum_skeleton_twosided():
    return "enum { doSkeletonTwoSided = true };"


@class_member(classtag="operator")
def enum_is_linear():
    linear = is_linear()
    if linear:
        return "enum { isLinear = true };"
    else:
        return "enum { isLinear = false };"


def name_initree_member():
    define_initree("_iniParams")
    return "_iniParams"


@class_basename(classtag="operator")
def localoperator_basename(form_ident):
    return get_form_option("classname", form_ident)


@class_member(classtag="operator")
def typedef_coefficient_vector(name, coeff):
    gfs_type = type_gridfunctionspace_template_parameter(coeff)
    return "using {} = Dune::PDELab::Backend::Vector<{}, {}>;".format(name, gfs_type, type_floatingpoint())


def type_coefficient_vector(coeff):
    name = "Coefficient_Vector_{}".format(coeff.count())
    typedef_coefficient_vector(name, coeff)
    return name


@class_member(classtag="operator")
def localoperator_set_coefficient(vector_name, gfs_name, coeff, restriction):
    from dune.codegen.pdelab.driver.gridoperator import _cf_ident
    method_name = "setCoefficient{}".format(_cf_ident(coeff))

    gfs_argument = "p_gfs"
    gfs_type = type_gridfunctionspace_template_parameter(coeff)
    vector_argument = "p_coefficient_vector"
    vector_type = type_coefficient_vector(coeff)
    lfs_name = name_coefficient_lfs(coeff, restriction)
    lfs_type = type_coefficient_lfs(coeff)
    lfs_cache_name = name_coefficient_lfs_cache(coeff, restriction)
    lfs_cache_type = type_coefficient_lfs_cache(coeff)
    return ["void {}(std::shared_ptr<const {}> {}, std::shared_ptr<{}> {}){{".format(method_name,
                                                                                     gfs_type,
                                                                                     gfs_argument,
                                                                                     vector_type,
                                                                                     vector_argument),
            "  {} = {};".format(gfs_name, gfs_argument),
            "  {} = {};".format(vector_name, vector_argument),
            "  {} = std::make_shared<{}>(*{});".format(lfs_name, lfs_type, gfs_name),
            "  {} = std::make_shared<{}>(*{});".format(lfs_cache_name, lfs_cache_type, lfs_name),
            "}"]


@class_member(classtag="operator")
def declare_coefficient_vector(name, coeff):
    vector_type = type_coefficient_vector(coeff)
    return "mutable std::shared_ptr<{}> {};".format(vector_type, name)


def name_coefficient_vector(coeff, restriction):
    # We reuse the grid function for volume integrals in skeleton integrals
    if restriction == Restriction.POSITIVE:
        restriction = Restriction.NONE
    restr = "_n" if restriction == Restriction.NEGATIVE else ""
    vector_name = "coefficient_vector_{}{}".format(coeff.count(), restr)
    declare_coefficient_vector(vector_name, coeff)
    gfs_name = name_coefficient_gfs(coeff, restriction)
    localoperator_set_coefficient(vector_name, gfs_name, coeff, restriction)
    return vector_name


@class_member(classtag="operator")
def typedef_coefficient_lfs(lfs_name, coeff):
    gfs_type = type_gridfunctionspace_template_parameter(coeff)
    return "using {} = Dune::PDELab::LocalFunctionSpace<{}>;".format(lfs_name, gfs_type)


def type_coefficient_lfs(coeff):
    lfs_name = "Coefficient_LFS{}".format(coeff.count())
    typedef_coefficient_lfs(lfs_name, coeff)
    return lfs_name


@class_member(classtag="operator")
def declare_coefficient_lfs(lfs_name, coeff):
    lfs_type = type_coefficient_lfs(coeff)
    return "mutable std::shared_ptr<{}> {};".format(lfs_type, lfs_name)


def name_coefficient_lfs(coeff, restriction):
    restr = "_n" if restriction == Restriction.NEGATIVE else ""
    lfs_name = "coefficient_lfs_{}{}".format(coeff.count(), restr)
    declare_coefficient_lfs(lfs_name, coeff)
    from dune.codegen.pdelab.spaces import bind_lfs
    bind_lfs(lfs_name, restriction)
    return lfs_name


@class_member(classtag="operator")
def typedef_coefficient_lfs_cache(lfs_cache_name, coeff):
    lfs_type = type_coefficient_lfs(coeff)
    return "using {} = Dune::PDELab::LFSIndexCache<{}>;".format(lfs_cache_name, lfs_type)


def type_coefficient_lfs_cache(coeff):
    lfs_cache_name = "Coefficient_LFS_Cache{}".format(coeff.count())
    typedef_coefficient_lfs_cache(lfs_cache_name, coeff)
    return lfs_cache_name


@class_member(classtag="operator")
def declare_coefficient_lfs_cache(lfs_cache_name, coeff):
    lfs_cache_type = type_coefficient_lfs_cache(coeff)
    return "mutable std::shared_ptr<{}> {};".format(lfs_cache_type, lfs_cache_name)


def name_coefficient_lfs_cache(coeff, restriction):
    # We reuse the grid function for volume integrals in skeleton integrals
    if restriction == Restriction.POSITIVE:
        restriction = Restriction.NONE
    restr = "_n" if restriction == Restriction.NEGATIVE else ""
    lfs_cache_name = "coefficient_lfs_cache_{}{}".format(coeff.count(), restr)
    declare_coefficient_lfs_cache(lfs_cache_name, coeff)
    return lfs_cache_name


@class_member(classtag="operator")
def declare_coefficient_gfs(name, coeff):
    gfs_type = type_gridfunctionspace_template_parameter(coeff)
    return "mutable std::shared_ptr<const {}> {};".format(gfs_type, name)


def name_coefficient_gfs(coeff, restriction):
    # We reuse the grid function for volume integrals in skeleton integrals
    if restriction == Restriction.POSITIVE:
        restriction = Restriction.NONE
    restr = "_n" if restriction == Restriction.NEGATIVE else ""
    gfs_name = "coefficient_gfs_{}{}".format(coeff.count(), restr)
    declare_coefficient_gfs(gfs_name, coeff)
    return gfs_name


@template_parameter(classtag="operator")
def type_gridfunctionspace_template_parameter(coeff):
    name = "GFS_COEFF_{}".format(coeff.count())
    return name


def class_type_from_cache(classtag):
    from dune.codegen.generation import retrieve_cache_items

    # get the basename
    basename = [i for i in retrieve_cache_items(condition="{} and basename".format(classtag))]
    assert len(basename) == 1
    basename = basename[0]

    # get the template parameters
    tparams = [i for i in retrieve_cache_items(condition="{} and template_param".format(classtag))]
    tparam_str = ''
    if len(tparams) > 0:
        tparam_str = '<{}>'.format(', '.join(t for t in tparams))

    return basename, basename + tparam_str


class AccumulationSpace(Record):
    def __init__(self,
                 lfs=None,
                 index=None,
                 restriction=None,
                 element=None,
                 ):
        Record.__init__(self,
                        lfs=lfs,
                        index=index,
                        restriction=restriction,
                        element=element,
                        )

    def get_args(self):
        if self.lfs is None:
            return ()
        else:
            return (self.lfs, self.index)

    def get_restriction(self):
        if self.restriction is None:
            return ()
        else:
            return (self.restriction,)


# TODO maybe move this onto the visitor as a helper function?
def determine_accumulation_space(info, number):
    if info is None:
        return AccumulationSpace()

    assert info is not None
    element = info.element
    subel = element
    from ufl import MixedElement
    if isinstance(element, MixedElement):
        subel = element.extract_component(info.element_index)[1]

    # And generate a local function space for it!
    from dune.codegen.pdelab.spaces import name_lfs, lfs_iname
    lfs = name_lfs(element, info.restriction, info.element_index)
    from dune.codegen.generation import valuearg
    from loopy.types import NumpyType
    valuearg(lfs, dtype=NumpyType("str"))

    if get_form_option("blockstructured"):
        from dune.codegen.blockstructured.tools import micro_index_to_macro_index
        from dune.codegen.blockstructured.spaces import lfs_inames
        lfsi = micro_index_to_macro_index(subel, lfs_inames(subel, info.restriction, count=number))
    else:
        from dune.codegen.pdelab.spaces import lfs_inames
        lfsi = Variable(lfs_iname(subel, info.restriction, count=number))

    # If the LFS is not yet a pymbolic expression, make it one
    from pymbolic.primitives import Expression
    if not isinstance(lfs, Expression):
        lfs = Variable(lfs)

    return AccumulationSpace(lfs=lfs,
                             index=lfsi,
                             restriction=info.restriction,
                             element=subel
                             )


def boundary_predicates(measure, subdomain_id):
    predicates = []

    if subdomain_id not in ['everywhere', 'otherwise']:
        # Get the original form and inspect the present measures
        from dune.codegen.generation import get_global_context_value
        data = get_global_context_value("data")
        original_form = data.object_by_name[get_form_option("form")]

        subdomains = []
        for integral in original_form.integrals():
            if integral.integral_type() == measure and integral.subdomain_id() == subdomain_id:
                subdomains.append(integral.subdomain_data())

        subdomain_data, = set(subdomains)

        from ufl.classes import Expr
        if isinstance(subdomain_data, Expr):
            visitor = get_visitor(measure, subdomain_id)
            subdomain_data = visitor(subdomain_data, do_predicates=True)

        p = prim.Comparison(subdomain_data, '==', subdomain_id)

        # Try to find conditions that are always 0 or always 1
        from pymbolic.mapper.evaluator import evaluate
        try:
            eval = evaluate(p)
            if not eval:
                return frozenset({False})
        except:
            predicates.append(p)

    return frozenset(predicates)


@accumulation_mixin("base")
class AccumulationMixinBase(object):
    def get_accumulation_info(self, expr):
        raise NotImplementedError

    def list_accumulation_infos(self, expr):
        raise NotImplementedError

    def generate_accumulation_instruction(self, expr):
        raise NotImplementedError


@accumulation_mixin("generic")
class GenericAccumulationMixin(AccumulationMixinBase):
    def get_accumulation_info(self, expr):
        restriction = self.restriction
        if self.measure == 'exterior_facet':
            restriction = Restriction.POSITIVE

        return get_accumulation_info(expr, restriction, self.indices, self)

    def list_accumulation_infos(self, expr):
        return list_accumulation_infos(expr, self)

    def generate_accumulation_instruction(self, expr):
        return generate_accumulation_instruction(expr, self)


class PDELabAccumulationInfo(ImmutableRecord):
    def __init__(self,
                 element=None,
                 element_index=0,
                 restriction=None,
                 inames=(),
                 ):
        ImmutableRecord.__init__(self,
                                 element=element,
                                 element_index=element_index,
                                 restriction=restriction,
                                 inames=inames,
                                 )

    def __eq__(self, other):
        return type(self) == type(other) and self.element_index == other.element_index and self.restriction == other.restriction

    def __hash__(self):
        return (self.element_index, self.restriction)


def _list_infos(expr, number, visitor):
    from dune.codegen.ufl.modified_terminals import extract_modified_arguments
    ma = extract_modified_arguments(expr, argnumber=number)
    if len(ma) == 0:
        if number == 1:
            yield None
        return
    element = ma[0].argexpr.ufl_element()

    if visitor.measure == "cell":
        restrictions = (Restriction.NONE,)
    elif visitor.measure == "exterior_facet":
        restrictions = (Restriction.POSITIVE,)
    elif visitor.measure == "interior_facet":
        restrictions = (Restriction.POSITIVE, Restriction.NEGATIVE)
    for res in restrictions:
        for ei in range(element.value_size()):
            yield PDELabAccumulationInfo(element_index=ei, restriction=res)


def list_accumulation_infos(expr, visitor):
    testgen = _list_infos(expr, 0, visitor)
    trialgen = _list_infos(expr, 1, visitor)

    import itertools
    return itertools.product(testgen, trialgen)


@kernel_cached
def get_accumulation_info(expr, restriction, indices, visitor):
    element = expr.ufl_element()
    leaf_element = element
    element_index = 0
    from ufl import MixedElement
    if isinstance(expr.ufl_element(), MixedElement):
        element_index = indices[0]
        leaf_element = element.extract_component(element_index)[1]

    inames = visitor.lfs_inames(leaf_element,
                                restriction,
                                expr.number()
                                )

    return PDELabAccumulationInfo(element=expr.ufl_element(),
                                  element_index=element_index,
                                  restriction=restriction,
                                  inames=inames,
                                  )


def generate_accumulation_instruction(expr, visitor):
    # Collect the lfs and lfs indices for the accumulate call
    test_lfs = determine_accumulation_space(visitor.test_info, 0)

    # In the jacobian case, also determine the space for the ansatz space
    ansatz_lfs = determine_accumulation_space(visitor.trial_info, 1)

    # Collect the lfs and lfs indices for the accumulate call
    from dune.codegen.pdelab.argument import name_accumulation_variable
    accumvar = name_accumulation_variable(test_lfs.get_restriction() + ansatz_lfs.get_restriction())

    predicates = boundary_predicates(visitor.measure, visitor.subdomain_id)
    rank = 1 if ansatz_lfs.lfs is None else 2

    from dune.codegen.pdelab.argument import PDELabAccumulationFunction
    from pymbolic.primitives import Call
    accexpr = Call(PDELabAccumulationFunction(accumvar, rank),
                   (test_lfs.get_args() + ansatz_lfs.get_args() + (expr,))
                   )

    from dune.codegen.generation import instruction
    quad_inames = visitor.quadrature_inames()
    lfs_inames = frozenset(visitor.test_info.inames)
    if visitor.trial_info:
        lfs_inames = lfs_inames.union(visitor.trial_info.inames)

    deps = lp.symbolic.DependencyMapper()(accexpr)
    deps = frozenset({Writes(get_pymbolic_basename(d)) for d in deps})

    instruction(assignees=(),
                expression=accexpr,
                forced_iname_deps=lfs_inames.union(frozenset(quad_inames)),
                forced_iname_deps_is_final=True,
                predicates=predicates,
                depends_on=deps,
                )


def get_visitor(measure, subdomain_id, **kwargs):
    # Construct the visitor taking into account geometry mixins
    from dune.codegen.ufl.visitor import UFL2LoopyVisitor
    mixins = get_form_option("geometry_mixins").split(",")
    VisitorType = construct_from_mixins(base=UFL2LoopyVisitor, mixins=mixins, mixintype="geometry", name="UFLVisitor")

    # Mix quadrature mixins in
    mixins = get_form_option("quadrature_mixins").split(",")
    VisitorType = construct_from_mixins(base=VisitorType, mixins=mixins, mixintype="quadrature", name="UFLVisitor")

    # Mix basis mixins in
    mixins = get_form_option("basis_mixins").split(",")
    VisitorType = construct_from_mixins(base=VisitorType, mixins=mixins, mixintype="basis", name="UFLVisitor")

    # Mix accumulation mixins in
    mixins = get_form_option("accumulation_mixins").split(",")
    VisitorType = construct_from_mixins(base=VisitorType, mixins=mixins, mixintype="accumulation", name="UFLVisitor")

    return VisitorType(measure, subdomain_id, **kwargs)


def visit_integral(integral):
    integrand = integral.integrand()
    measure = integral.integral_type()
    subdomain_id = integral.subdomain_id()

    # Avoid even visiting the integral, if it is noop
    predicates = boundary_predicates(measure, subdomain_id)
    if False in predicates:
        return

    # Start the visiting process!
    visitor = get_visitor(measure, subdomain_id)
    with global_context(visitor=visitor):
        visitor.accumulate(integrand)

    run_hook(name="after_visit",
             args=(visitor,),
             )


def generate_kernel(integrals):
    logger = logging.getLogger(__name__)

    # Assert that metadata for a given measure type agrees. This is a limitation
    # of our current approach that is hard to overcome.
    def remove_nonuser_metadata(d):
        return frozendict({k: v for k, v in d.items() if k != "estimated_polynomial_degree"})

    meta_dicts = [remove_nonuser_metadata(i.metadata()) for i in integrals]
    if len(set(meta_dicts)) > 1:
        measure = get_global_context_value("measure")
        raise CodegenUFLError("Measure {} used with varying metadata! dune-codegen does not currently support this.")

    with form_option_context(**meta_dicts[0]):
        # Visit all integrals once to collect information (dry-run)!
        logger.debug('generate_kernel: visit_integrals (dry run)')
        with global_context(dry_run=True):
            for integral in integrals:
                visit_integral(integral)

        # Now perform some checks on what should be done
        from dune.codegen.sumfact.vectorization import decide_vectorization_strategy
        logger.debug('generate_kernel: decide_vectorization_strategy')
        decide_vectorization_strategy()

        # Delete the cache contents and do the real thing!
        logger.debug('generate_kernel: visit_integrals (no dry run)')
        from dune.codegen.generation import delete_cache_items
        delete_cache_items("kernel_default")
        for integral in integrals:
            visit_integral(integral)

    from dune.codegen.pdelab.signatures import kernel_name, assembly_routine_signature
    name = kernel_name()
    signature = assembly_routine_signature()
    knl = extract_kernel_from_cache("kernel_default", name, signature)
    delete_cache_items("kernel_default")

    # Reset the quadrature degree
    from dune.codegen.sumfact.tabulation import set_quadrature_points
    set_quadrature_points(None)

    # Clean the cache from any data collected after the dry run
    delete_cache_items("dryrundata")

    # Run preprocessing from custom user code
    knl = run_hook(name="loopy_kernel",
                   args=(ReturnArg(knl),),
                   )

    return knl


def generate_kernels_per_integral(integrals):
    if get_form_option("sumfact"):
        from dune.codegen.sumfact.switch import sumfact_generate_kernels_per_integral
        for k in sumfact_generate_kernels_per_integral(integrals):
            yield k
    else:
        yield generate_kernel(integrals)


def extract_kernel_from_cache(tag, name, signature, wrap_in_cgen=True, add_timings=True, constructor_preamble_order=None):
    # Now extract regular loopy kernel components
    from dune.codegen.loopy.target import DuneTarget
    domains = [i for i in retrieve_cache_items("{} and domain".format(tag))]

    if not domains:
        domains = ["{[stupid] : 0<=stupid<1}"]

    instructions = [i for i in retrieve_cache_items("{} and instruction".format(tag))]
    substrules = [i for i in retrieve_cache_items("{} and substrule".format(tag)) if i is not None]
    temporaries = {i.name: i for i in retrieve_cache_items("{} and temporary".format(tag))}
    arguments = [i for i in retrieve_cache_items("{} and argument".format(tag))]
    silenced = [l for l in retrieve_cache_items("{} and silenced_warning".format(tag))]
    transformations = [t for t in retrieve_cache_items("{} and transformation".format(tag))]

    # Construct an options object
    from loopy import Options
    opt = Options(ignore_boostable_into=True,
                  check_dep_resolution=False,
                  enforce_variable_access_ordered=True,
                  )

    # Create the kernel
    from loopy import make_kernel, preprocess_kernel
    kernel = make_kernel(domains,
                         instructions + substrules,
                         arguments,
                         temporary_variables=temporaries,
                         target=DuneTarget(),
                         options=opt,
                         silenced_warnings=silenced,
                         name=name,
                         lang_version=(2018, 2),
                         )
    from loopy import make_reduction_inames_unique
    kernel = make_reduction_inames_unique(kernel)

    # Apply the transformations that were gathered during tree traversals
    for trafo in transformations:
        kernel = trafo[0](kernel, *trafo[1], **trafo[2])

    # Apply performance transformations
    from dune.codegen.loopy.transformations.performance import performance_transformations
    kernel = performance_transformations(kernel, signature)

    from dune.codegen.loopy import heuristic_duplication
    kernel = heuristic_duplication(kernel)

    # Maybe apply vectorization strategies
    if get_form_option("vectorization_quadloop") and get_form_option("sumfact"):
        from dune.codegen.loopy.transformations.vectorize_quad import vectorize_quadrature_loop
        kernel = vectorize_quadrature_loop(kernel)

    if get_form_option("vectorization_blockstructured"):
        from dune.codegen.blockstructured.vectorization import vectorize_micro_elements
        kernel = vectorize_micro_elements(kernel)

    from dune.codegen.loopy.transformations.constant_folding import apply_constant_folding
    kernel = apply_constant_folding(kernel)

    # Now add the preambles to the kernel
    if constructor_preamble_order:
        def add_section(section_tag):
            content = []
            tagcontents = [i for i in retrieve_cache_items("preamble and {} and {}".format(tag, section_tag))]
            if tagcontents:
                content.append("// {}".format(section_tag.capitalize()))
                content.extend(tagcontents)
                content.append("")
            return content

        preambles = []
        for section in constructor_preamble_order:
            preambles = preambles + add_section(section)
        preambles = [(i, p) for i, p in enumerate(preambles)]
    else:
        preambles = [(i, p) for i, p in enumerate(retrieve_cache_items("{} and preamble".format(tag)))]
    kernel = kernel.copy(preambles=preambles)

    # Remove inames that have become obsolete
    kernel = lp.remove_unused_inames(kernel)

    # Do the loopy preprocessing!
    kernel = preprocess_kernel(kernel)

    # *REALLY* ignore boostability. This is - so far - necessary due to a mystery bug.
    kernel = kernel.copy(instructions=[i.copy(boostable=False, boostable_into=frozenset()) for i in kernel.instructions])

    from dune.codegen.loopy.transformations.matchfma import match_fused_multiply_add
    kernel = match_fused_multiply_add(kernel)

    # Add instrumentation to the kernel
    from dune.codegen.loopy.transformations.instrumentation import add_instrumentation
    if add_timings and get_form_option("sumfact"):
        from dune.codegen.pdelab.signatures import assembler_routine_name
        kernel = add_instrumentation(kernel, lp.match.Tagged("sumfact_stage1"), "{}_kernel_stage1".format(assembler_routine_name()), 4)
        kernel = add_instrumentation(kernel, lp.match.Tagged("sumfact_stage2"), "{}_kernel_quadratureloop".format(assembler_routine_name()), 4, depends_on=frozenset({lp.match.Tagged("sumfact_stage1")}))
        kernel = add_instrumentation(kernel, lp.match.Tagged("sumfact_stage3"), "{}_kernel_stage3".format(assembler_routine_name()), 4, depends_on=frozenset({lp.match.Tagged("sumfact_stage2")}))

    # Apply cse transformation
    from dune.codegen.loopy.transformations.cse import cse
    if get_form_option("apply_cse"):
        kernel = cse(kernel)

    if wrap_in_cgen:
        # Wrap the kernel in something which can generate code
        if signature is None:
            from dune.codegen.pdelab.signatures import assembly_routine_signature
            signature = assembly_routine_signature()
        kernel = LoopyKernelMethod(signature, kernel, add_timings=add_timings)

    return kernel


def name_time_dumper_os():
    return "os"


def name_time_dumper_reset():
    return "reset"


def name_time_dumper_ident():
    return "ident"


@generator_factory(item_tags=("cached",), cache_key_generator=lambda **kw: None)
def name_example_kernel(name=None):
    return name


class TimerMethod(ClassMember):
    def __init__(self):
        os = name_time_dumper_os()
        reset = name_time_dumper_reset()
        ident = name_time_dumper_ident()
        knl = name_example_kernel()
        assert(knl is not None)

        content = ["template <typename Stream>",
                   "void dump_timers(Stream& {}, std::string {}, bool {})".format(os, ident, reset),
                   "{"]
        dump_timers = [i for i in retrieve_cache_items(condition='dump_timers')]
        content.extend(map(lambda x: '  ' + x, dump_timers))
        content.append("}")
        ClassMember.__init__(self, content)


class RegisterLikwidMethod(ClassMember):
    def __init__(self):
        knl = name_example_kernel()
        assert(knl is not None)

        content = ["void register_likwid_timers()"
                   "{"]
        register_liwkid_timers = [i for i in retrieve_cache_items(condition='register_likwid_timers')]
        content.extend(map(lambda x: '  ' + x, register_liwkid_timers))
        content += ["}"]
        ClassMember.__init__(self, content)


class RegisterSSCMarksMethod(ClassMember):
    def __init__(self):
        knl = name_example_kernel()
        assert(knl is not None)

        content = ["void dump_ssc_marks()"
                   "{"]
        register_liwkid_timers = [i for i in retrieve_cache_items(condition='register_ssc_marks')]
        content.extend(map(lambda x: '  ' + x, register_liwkid_timers))
        content += ["}"]
        ClassMember.__init__(self, content)


class LoopyKernelMethod(ClassMember):
    def __init__(self, signature, kernel, add_timings=True, initializer_list=[]):
        from loopy import generate_body
        from cgen import LiteralLines, Block
        content = signature

        # Add initializer list if this is a constructor
        if initializer_list:
            content[-1] = content[-1] + " :"
            for init in initializer_list[:-1]:
                content.append(" " * 4 + init + ",")
            content.append(" " * 4 + initializer_list[-1])

        content.append('{')
        if kernel is not None:
            # Start timer
            if add_timings and get_option('instrumentation_level') >= 3:
                from dune.codegen.pdelab.signatures import assembler_routine_name
                timer_name = assembler_routine_name() + '_kernel'
                name_example_kernel(name=timer_name)

                if get_option('use_likwid'):
                    from dune.codegen.pdelab.driver.timings import init_likwid_timer
                    include_file("likwid.h", filetag="operatorfile")
                    init_likwid_timer(timer_name)
                    content.append('  ' + 'LIKWID_MARKER_START(\"{}\");'.format(timer_name))
                    register_liwkid_timer(timer_name)
                elif get_option('use_sde'):
                    from dune.codegen.pdelab.driver.timings import get_region_marks, ssc_macro
                    post_include(ssc_macro(), filetag='operatorfile')
                    marks = get_region_marks(timer_name, driver=False)
                    content.append('  ' + '__SSC_MARK(0x{});'.format(marks[0]))
                    dump_ssc_marks(timer_name)
                else:
                    post_include('HP_DECLARE_TIMER({});'.format(timer_name), filetag='operatorfile')
                    content.append('  ' + 'HP_TIMER_START({});'.format(timer_name))
                    dump_accumulate_timer(timer_name)

                if add_timings and get_option("instrumentation_level") >= 4:
                    setuptimer = '{}_kernel_setup'.format(assembler_routine_name())
                    if get_option('use_likwid'):
                        from dune.codegen.pdelab.driver.timings import init_likwid_timer
                        init_likwid_timer(setuptimer)
                        content.append('  ' + 'LIKWID_MARKER_START(\"{}\");'.format(setuptimer))
                        register_liwkid_timer(setuptimer)
                    elif get_option('use_sde'):
                        from dune.codegen.pdelab.driver.timings import get_region_marks
                        setup_marks = get_region_marks(setuptimer, driver=False)
                        content.append('  ' + '__SSC_MARK(0x{});'.format(setup_marks[0]))
                        dump_ssc_marks(setuptimer)
                    else:
                        post_include('HP_DECLARE_TIMER({});'.format(setuptimer), filetag='operatorfile')
                        content.append('  HP_TIMER_START({});'.format(setuptimer))
                        dump_accumulate_timer(setuptimer)

            # Add kernel preamble
            for i, p in kernel.preambles:
                content.append('  ' + p)

            if add_timings and get_option('instrumentation_level') >= 4:
                if get_option('use_likwid'):
                    content.append('  ' + 'LIKWID_MARKER_STOP(\"{}\");'.format(setuptimer))
                elif get_option('use_sde'):
                    content.append('  ' + '__SSC_MARK(0x{});'.format(setup_marks[1]))
                else:
                    content.append('  ' + 'HP_TIMER_STOP({});'.format(setuptimer))

            # Add kernel body
            content.extend(l for l in generate_body(kernel).split('\n')[1:-1])

            # Stop timer
            if add_timings and get_option('instrumentation_level') >= 3:
                if get_option('use_likwid'):
                    content.append('  ' + 'LIKWID_MARKER_STOP(\"{}\");'.format(timer_name))
                elif get_option('use_sde'):
                    content.append('  ' + '__SSC_MARK(0x{});'.format(marks[1]))
                else:
                    content.append('  ' + 'HP_TIMER_STOP({});'.format(timer_name))

        content.append('}')
        ClassMember.__init__(self, content, name=kernel.name if kernel is not None else "")


def cgen_class_from_cache(tag, members=[], constructor_preamble_order=None):
    from dune.codegen.generation import retrieve_cache_items

    # Run a hook before we start extracting the class from the generation cache
    run_hook(name="operator_class_extraction")

    # Sort the given member functions by their name to help debugging by fixing
    # the order
    members = sorted(members, key=lambda m: m.name)

    # Generate the name by concatenating basename and template parameters
    basename, fullname = class_type_from_cache(tag)

    base_classes = [bc for bc in retrieve_cache_items('{} and baseclass'.format(tag))]
    constructor_params = [bc for bc in retrieve_cache_items('{} and constructor_param'.format(tag))]
    il = [i for i in retrieve_cache_items('{} and initializer'.format(tag))]
    pm = [m for m in retrieve_cache_items('{} and member'.format(tag))]
    tparams = [i for i in retrieve_cache_items('{} and template_param'.format(tag))]

    # Construct the constructor
    with form_option_context(apply_cse=False):
        constructor_knl = extract_kernel_from_cache(tag,
                                                    "constructor_kernel",
                                                    None,
                                                    wrap_in_cgen=False,
                                                    add_timings=False,
                                                    constructor_preamble_order=constructor_preamble_order)
    from dune.codegen.loopy.target import DuneTarget
    constructor_knl = constructor_knl.copy(target=DuneTarget(declare_temporaries=False))
    signature = "{}({})".format(basename, ", ".join(next(iter(p.generate(with_semicolon=False))) for p in constructor_params))
    constructor = LoopyKernelMethod([signature], constructor_knl, add_timings=False, initializer_list=il)

    from loopy import get_one_scheduled_kernel
    constructor_knl = get_one_scheduled_kernel(constructor_knl)

    # Take any temporary declarations from the kernel and make them class members
    target = DuneTarget()
    from loopy.codegen import CodeGenerationState
    codegen_state = CodeGenerationState(kernel=constructor_knl,
                                        implemented_data_info=None,
                                        implemented_domain=None,
                                        implemented_predicates=frozenset(),
                                        seen_dtypes=frozenset(),
                                        seen_functions=frozenset(),
                                        seen_atomic_dtypes=frozenset(),
                                        var_subst_map={},
                                        allow_complex=False,
                                        is_generating_device_code=True,
                                        )
    decls = [cgen.Line("\n  " + next(iter(d.generate()))) for d in target.get_device_ast_builder().get_temporary_decls(codegen_state, 0)]

    from dune.codegen.cgen import Class
    return Class(basename, base_classes=base_classes, members=[constructor] + pm + members + decls, tparam_decls=tparams)


def local_operator_default_settings(operator, form):
    # Manage includes and base classes that we always need
    include_file('dune/pdelab/gridfunctionspace/gridfunctionspace.hh', filetag="operatorfile")
    include_file('dune/pdelab/localoperator/idefault.hh', filetag="operatorfile")
    include_file('dune/pdelab/localoperator/flags.hh', filetag="operatorfile")
    include_file('dune/pdelab/localoperator/pattern.hh', filetag="operatorfile")

    post_include("#pragma GCC diagnostic push", filetag="operatorfile")
    post_include("#pragma GCC diagnostic ignored \"-Wsign-compare\"", filetag="operatorfile")
    post_include("#pragma GCC diagnostic ignored \"-Wunused-variable\"", filetag="operatorfile")
    post_include("#pragma GCC diagnostic ignored \"-Wunused-but-set-variable\"", filetag="operatorfile")
    end_of_file("#pragma GCC diagnostic pop", filetag="operatorfile")

    # Trigger this one once early on to assure that template
    # parameters are set in the right order
    localoperator_basename(operator)
    lop_template_ansatz_gfs()
    lop_template_test_gfs()

    # Make sure there is always the same constructor arguments, even if some of them are
    # not strictly needed. Also ensure the order.
    name_initree_member()

    # Iterate over the needed grid functions in correct order
    for c in sorted(filter(lambda c: c.count() > 2, form.coefficients()), key=lambda c: c.count()):
        # Omit those coefficients that are handled from user code.
        # TODO: This whole problem of deterministic order of constructor arguments
        #       should be solved properly of course.
        if hasattr(c, "visit"):
            continue
        type_gridfunctionspace_template_parameter(c)

    # Add right base classes for stationary/instationary operators
    base_class('Dune::PDELab::LocalOperatorDefaultFlags', classtag="operator")
    from dune.codegen.pdelab.driver import is_stationary
    if not is_stationary():
        rf = type_floatingpoint()
        base_class('Dune::PDELab::InstationaryLocalOperatorDefaultMethods<{}>'
                   .format(rf), classtag="operator")

    # *always* add the volume pattern, PDELab cannot handle matrices without diagonal blocks
    with global_context(integral_type="cell"):
        enum_pattern()
        pattern_baseclass()

    # For non-linear local operators we need to set the isLinear flag to false
    enum_is_linear()

    if get_form_option("block_preconditioner_diagonal") or get_form_option("block_preconditioner_pointdiagonal"):
        enum_skeleton_twosided()


def measure_is_enabled(measure):
    option_dict = {"cell": "enable_volume",
                   "interior_facet": "enable_skeleton",
                   "exterior_facet": "enable_boundary",
                   }

    return get_form_option(option_dict[measure])


def generate_residual_kernels(form, original_form):
    if not get_form_option("generate_residuals"):
        return {}

    if get_form_option("block_preconditioner_pointdiagonal"):
        from ufl import derivative
        jacform = derivative(original_form, original_form.coefficients()[0])

        from dune.codegen.ufl.preprocess import preprocess_form
        jacform = preprocess_form(jacform).preprocessed_form

        from dune.codegen.ufl.transformations.blockpreconditioner import diagonal_block_jacobian
        form = diagonal_block_jacobian(jacform)

    if get_form_option("blockstructured_preconditioner"):
        from dune.codegen.blockstructured.preconditioner import generate_preconditioner_files
        generate_preconditioner_files(form, original_form)

    logger = logging.getLogger(__name__)
    with global_context(form_type='residual'):
        operator_kernels = {}

        # Generate the necessary residual methods
        for measure in set(i.integral_type() for i in form.integrals()):
            logger.info("generate_residual_kernels: measure {}".format(measure))

            if not measure_is_enabled(measure):
                continue

            with global_context(integral_type=measure):
                from dune.codegen.pdelab.signatures import assembler_routine_name
                with global_context(kernel=assembler_routine_name()):
                    kernel = [k for k in generate_kernels_per_integral(form.integrals_by_type(measure))]

                # The integrals might vanish due to unfulfillable boundary conditions.
                # We only generate the local operator enums/base classes if they did not.
                if kernel:
                    enum_pattern()
                    pattern_baseclass()
                    enum_alpha()

                # Maybe add numerical differentiation
                if get_form_option("numerical_jacobian"):
                    # Include headers for numerical methods
                    include_file("dune/pdelab/localoperator/defaultimp.hh", filetag="operatorfile")

                    # Numerical jacobian base class
                    _, loptype = class_type_from_cache("operator")
                    from dune.codegen.pdelab.signatures import ufl_measure_to_pdelab_measure
                    which = ufl_measure_to_pdelab_measure(measure)
                    base_class("Dune::PDELab::NumericalJacobian{}<{}>".format(which, loptype), classtag="operator")

                    # Numerical jacobian initializer list
                    ini = name_initree_member()
                    ini_constructor = name_initree_constructor_param()
                    initializer_list("Dune::PDELab::NumericalJacobian{}<{}>".format(which, loptype),
                                     ["{}.get<double>(\"numerical_epsilon.{}\", 1e-9)".format(ini_constructor, ini, which.lower())],
                                     classtag="operator",
                                     )

                    # In the case of matrix free operator evaluation we need jacobian apply methods
                    if get_form_option("generate_jacobian_apply"):
                        from dune.codegen.pdelab.driver import is_linear
                        if is_linear(original_form):
                            # Numeical jacobian apply base class
                            base_class("Dune::PDELab::NumericalJacobianApply{}<{}>".format(which, loptype), classtag="operator")

                            # Numerical jacobian apply initializer list
                            initializer_list("Dune::PDELab::NumericalJacobianApply{}<{}>".format(which, loptype),
                                             ["{}.get<double>(\"numerical_epsilon.{}\", 1e-9)".format(ini_constructor, ini, which.lower())],
                                             classtag="operator",
                                             )
                        else:
                            # Numerical nonlinear jacobian apply base class
                            base_class("Dune::PDELab::NumericalNonlinearJacobianApply{}<{}>".format(which, loptype), classtag="operator")

                            # Numerical nonlinear jacobian apply initializer list
                            initializer_list("Dune::PDELab::NumericalNonlinearJacobianApply{}<{}>".format(which, loptype),
                                             ["{}.get<double>(\"numerical_epsilon.{}\", 1e-9)".format(ini_constructor, ini, which.lower())],
                                             classtag="operator",
                                             )

            operator_kernels[(measure, 'residual')] = kernel

        return operator_kernels


def generate_jacobian_kernels(form, original_form):
    logger = logging.getLogger(__name__)

    from ufl import derivative
    jacform = derivative(original_form, original_form.coefficients()[0])

    from dune.codegen.ufl.preprocess import preprocess_form
    jacform = preprocess_form(jacform).preprocessed_form

    if get_form_option("block_preconditioner_diagonal"):
        from dune.codegen.ufl.transformations.blockpreconditioner import diagonal_block_jacobian
        jacform = diagonal_block_jacobian(jacform)
    if get_form_option("block_preconditioner_offdiagonal"):
        from dune.codegen.ufl.transformations.blockpreconditioner import offdiagonal_block_jacobian
        jacform = offdiagonal_block_jacobian(jacform)

    operator_kernels = {}
    if get_form_option("generate_jacobian_apply"):
        # The apply vector has reserved index 1 so we directly use Coefficient class from ufl
        from ufl import Coefficient
        apply_coefficient = Coefficient(form.coefficients()[0].ufl_element(), 1)

        # Create application of jacobian on vector
        from ufl import action
        jac_apply_form = action(jacform, apply_coefficient)

        # Create kernel for jacobian application
        with global_context(form_type="jacobian_apply"):
            for measure in set(i.integral_type() for i in jac_apply_form.integrals()):
                with global_context(integral_type=measure):
                    from dune.codegen.pdelab.signatures import assembler_routine_name
                    with global_context(kernel=assembler_routine_name()):
                        kernel = [k for k in generate_kernels_per_integral(jac_apply_form.integrals_by_type(measure))]

                        if kernel:
                            enum_pattern()
                            pattern_baseclass()
                            enum_alpha()

                operator_kernels[(measure, 'jacobian_apply')] = kernel

                # Generate dummy functions for those kernels, that vanished in the differentiation process
                # We *could* solve this problem by using lambda_* terms but we do not really want that, so
                # we use empty jacobian assembly methods instead
                alpha_measures = set(i.integral_type() for i in form.integrals())
                jacobian_apply_measures = set(i.integral_type() for i in jac_apply_form.integrals())
                for it in alpha_measures - jacobian_apply_measures:
                    with global_context(integral_type=it):
                        from dune.codegen.pdelab.signatures import assembly_routine_signature
                        operator_kernels[(it, 'jacobian_apply')] = [LoopyKernelMethod(assembly_routine_signature(), kernel=None)]
    if get_form_option("generate_jacobians"):
        with global_context(form_type="jacobian"):
            with form_option_context(conditional=get_form_option("sumfact") and get_form_option("sumfact_regular_jacobians"),
                                     geometry_mixins="generic", quadrature_mixins="generic", basis_mixins="generic",
                                     accumulation_mixins="generic", sumfact=False):
                for measure in set(i.integral_type() for i in jacform.integrals()):
                    if not measure_is_enabled(measure):
                        continue

                    logger.info("generate_jacobian_kernels: measure {}".format(measure))
                    with global_context(integral_type=measure):
                        from dune.codegen.pdelab.signatures import assembler_routine_name
                        with global_context(kernel=assembler_routine_name()):
                            kernel = [k for k in generate_kernels_per_integral(jacform.integrals_by_type(measure))]

                            if kernel:
                                enum_pattern()
                                pattern_baseclass()
                                enum_alpha()

                    operator_kernels[(measure, 'jacobian')] = kernel

                # Generate dummy functions for those kernels, that vanished in the differentiation process
                # We *could* solve this problem by using lambda_* terms but we do not really want that, so
                # we use empty jacobian assembly methods instead
                alpha_measures = set(i.integral_type() for i in form.integrals())
                jacobian_measures = set(i.integral_type() for i in jacform.integrals())
                for it in alpha_measures - jacobian_measures:
                    with global_context(integral_type=it):
                        from dune.codegen.pdelab.signatures import assembly_routine_signature
                        operator_kernels[(it, 'jacobian')] = [LoopyKernelMethod(assembly_routine_signature(), kernel=None)]

    return operator_kernels


def generate_control_kernels(forms):
    # All forms will we written in the residual method and
    # accumulation will be done in a class member instead of the
    # residual.
    logger = logging.getLogger(__name__)
    with global_context(form_type='residual'):
        operator_kernels = {}

        # Generate the necessary residual methods
        for measure in set(i.integral_type() for form in forms for i in form.integrals()):
            if not measure_is_enabled(measure):
                continue

            logger.info("generate_control_kernels: measure {}".format(measure))
            with global_context(integral_type=measure):
                from dune.codegen.pdelab.signatures import assembler_routine_name
                with global_context(kernel=assembler_routine_name()):
                    # TODO: Sumfactorization not yet implemented
                    assert not get_form_option('sumfact')

                    from dune.codegen.pdelab.adjoint import control_generate_kernels_per_integral
                    forms_measure = [form.integrals_by_type(measure) for form in forms]
                    kernel = [k for k in control_generate_kernels_per_integral(forms_measure)]

                    # The integrals might vanish due to unfulfillable boundary conditions.
                    # We only generate the local operator enums/base classes if they did not.
                    if kernel:
                        enum_pattern()
                        pattern_baseclass()
                        enum_alpha()

            operator_kernels[(measure, 'residual')] = kernel

        return operator_kernels


def generate_localoperator_kernels(operator):
    logger = logging.getLogger(__name__)

    data = get_global_context_value("data")
    original_form = data.object_by_name[get_form_option("form")]
    from dune.codegen.ufl.preprocess import preprocess_form

    if get_form_option("adjoint"):
        # Generate adjoint operator
        #
        # The jacobian of the adjoint form is just the jacobian of the
        # original form with test and ansazt function swapped. A a
        # linear form you have to subtract the derivative of the
        # objective function w.r.t the ansatz function to get the
        # final residual formulation of the adjoint.
        #
        # Might not be true in all cases but works for the simple ones.
        assert get_form_option("objective_function") is not None
        assert get_form_option("control") is False

        from ufl import derivative, adjoint, action, replace
        from dune.codegen.ufl.execution import Coefficient

        # Jacobian of the adjoint form
        jacform = derivative(original_form, original_form.coefficients()[0])
        adjoint_jacform = adjoint(jacform)

        # Derivative of objective function w.r.t. state
        objective = data.object_by_name[get_form_option("objective_function")]
        objective_jacobian = derivative(objective, objective.coefficients()[0])

        # Replace coefficient belonging to ansatz function with new coefficient
        element = objective.coefficients()[0].ufl_element()
        coeff = Coefficient(element, count=3)
        objective_jacobian = replace(objective_jacobian, {objective.coefficients()[0]: coeff})
        if len(adjoint_jacform.coefficients()) > 0:
            adjoint_jacform = replace(adjoint_jacform, {adjoint_jacform.coefficients()[0]: coeff})

        # Residual of the adjoint form
        adjoint_form = action(adjoint_jacform, original_form.coefficients()[0])
        adjoint_form = adjoint_form + objective_jacobian

        # Update form and original_form
        original_form = adjoint_form
        form = preprocess_form(adjoint_form).preprocessed_form

    elif get_form_option("control"):
        # Generate control operator
        #
        # This is the normal form derived w.r.t. the control
        # variable. We generate a form for every row of:
        #
        # \nabla  \hat{J}(m) = (\nabla R(z,m))^T \lambda + \nabla_m J(z,m)
        #
        # These forms will not depend on the test function anymore and
        # will need special treatment for the accumulation process.
        from ufl import action, diff
        from dune.codegen.ufl.execution import Coefficient

        # Get control variables
        assert get_form_option("control_variable") is not None
        controls = [data.object_by_name[ctrl.strip()] for ctrl in get_form_option("control_variable").split(",")]

        # Transoform flat index to multiindex. Wrapper around numpy
        # unravel since we need to transform numpy ints to native
        # ints.
        def _unravel(flat_index, shape):
            multi_index = np.unravel_index(flat_index, shape)
            multi_index = tuple(int(i) for i in multi_index)
            return multi_index

        # Will be used to replace ansatz function with adjoint function
        element = original_form.coefficients()[0].ufl_element()
        coeff = Coefficient(element, count=3)

        # Store a form for every control
        forms = []
        for control in controls:
            shape = control.ufl_shape
            flat_length = int(np.prod(shape))
            for i in range(flat_length):
                c = control[_unravel(i, shape)]
                control_form = diff(original_form, c)
                control_form = action(control_form, coeff)
                objective = data.object_by_name[get_form_option("objective_function")]
                objective_gradient = diff(objective, c)
                control_form = control_form + objective_gradient
                forms.append(preprocess_form(control_form).preprocessed_form)

        # Used to create local operator default settings
        form = preprocess_form(original_form).preprocessed_form

    else:
        form = preprocess_form(original_form).preprocessed_form

    # Reset the generation cache
    from dune.codegen.generation import delete_cache_items
    delete_cache_items()

    # Have a data structure collect the generated kernels
    operator_kernels = {}

    # Generate things needed for all local operator files
    local_operator_default_settings(operator, form)

    if get_form_option("control"):
        logger.info("generate_localoperator_kernels: create methods for control operator")
        operator_kernels.update(generate_control_kernels(forms))
    else:
        logger.info("generate_localoperator_kernels: create residual methods")
        operator_kernels.update(generate_residual_kernels(form, original_form))

        # Generate the necessary jacobian methods
        if not get_form_option("numerical_jacobian"):
            logger.info("generate_localoperator_kernels: create jacobian methods")
            operator_kernels.update(generate_jacobian_kernels(form, original_form))

    # Return the set of generated kernels
    return operator_kernels


def generate_localoperator_file(kernels, filename):
    logger = logging.getLogger(__name__)

    operator_methods = []
    for k in kernels.values():
        operator_methods.extend(k)

    # Generate all the realizations of sum factorization kernel objects needed in this operator
    sfkernels = [sf for sf in retrieve_cache_items("kernelimpl")]
    if sfkernels:
        logger.info("generate_localoperator_kernels: Create {} sumfact kernel realizations".format(len(sfkernels)))

    from dune.codegen.sumfact.realization import realize_sumfact_kernel_function
    for sf, qp in sfkernels:
        from dune.codegen.sumfact.tabulation import set_quadrature_points
        set_quadrature_points(qp)
        operator_methods.append(realize_sumfact_kernel_function(sf))

    if get_option('instrumentation_level') >= 3:
        include_file('dune/codegen/common/timer.hh', filetag='operatorfile')
        if get_option('use_likwid'):
            operator_methods.append(RegisterLikwidMethod())
        elif get_option('use_sde'):
            operator_methods.append(RegisterSSCMarksMethod())
        else:
            operator_methods.append(TimerMethod())
    elif get_option('opcounter'):
        include_file('dune/codegen/common/timer.hh', filetag='operatorfile')

    # Write the file!
    from dune.codegen.file import generate_file
    # TODO take the name of this thing from the UFL file
    lop = cgen_class_from_cache("operator", members=operator_methods)
    generate_file(filename, "operatorfile", [lop])
