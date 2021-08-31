import logging

import numpy

from loopy import CallMangleInfo
from loopy.symbolic import FunctionIdentifier
from loopy.types import NumpyType

import pymbolic.primitives as prim

from dune.codegen.generation import (accumulation_mixin,
                                     class_member,
                                     constructor_parameter,
                                     function_mangler,
                                     get_global_context_value,
                                     global_context,
                                     globalarg,
                                     initializer_list,
                                     template_parameter,
                                     )
from dune.codegen.options import (get_form_option,
                                  )
from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.pdelab.localoperator import (boundary_predicates,
                                               determine_accumulation_space,
                                               extract_kernel_from_cache,
                                               GenericAccumulationMixin,
                                               get_visitor,
                                               )


@template_parameter(classtag="operator")
def type_dJdm():
    return "DJDM_VEC"


def name_dJdm_constructor_argument(name):
    _type = type_dJdm()
    constructor_name = name + "_"
    constructor_parameter("{}&".format(_type), constructor_name, classtag="operator")
    return constructor_name


@class_member(classtag="operator")
def define_dJdm_member(name):
    _type = type_dJdm()
    param = name_dJdm_constructor_argument(name)
    initializer_list(name, [param, ], classtag="operator")
    return "{}& {};".format(_type, name)


def generate_accumulation_instruction(expr, visitor, accumulation_index, number_of_controls):
    # Create class member dJdm for accumulating
    accumvar = "dJdm"
    shape = (number_of_controls,)
    define_dJdm_member(accumvar)

    # Tell loopy about
    globalarg(accumvar, shape=shape)
    assignee = prim.Subscript(prim.Variable(accumvar), accumulation_index)

    # We need to accumulate
    expr = prim.Sum((assignee, expr))

    from dune.codegen.generation import instruction
    quad_inames = visitor.quadrature_inames()
    instruction(assignee=assignee,
                expression=expr,
                forced_iname_deps=frozenset(quad_inames),
                forced_iname_deps_is_final=True,
                )


@accumulation_mixin("control")
class AdjointAccumulationMixin(GenericAccumulationMixin):
    def set_adjoint_information(self, accumulation_index, number_of_controls):
        self.accumulation_index = accumulation_index
        self.number_of_controls = number_of_controls

    def list_accumulation_infos(self, expr):
        return ["control"]

    def generate_accumulation_instruction(self, expr):
        return generate_accumulation_instruction(expr,
                                                 self,
                                                 self.accumulation_index,
                                                 self.number_of_controls)


def visit_integral(integral, accumulation_index, number_of_controls):
    integrand = integral.integrand()
    measure = integral.integral_type()
    subdomain_id = integral.subdomain_id()

    # The visitor needs to know about the current index and the number
    # of controls in order to generate the accumulation instruction
    visitor = get_visitor(measure, subdomain_id)
    visitor.set_adjoint_information(accumulation_index, number_of_controls)

    # Start the visiting process!
    visitor.accumulate(integrand)


def generate_kernel(forms):
    # Similar to the standard residual generation, except:
    # - Have multiple forms
    # - Pass index and number of forms along
    logger = logging.getLogger(__name__)

    # Visit all integrals once to collect information (dry-run)!
    logger.debug('generate_kernel: visit_integrals (dry run)')
    with global_context(dry_run=True):
        for i, form in enumerate(forms):
            for integral in form:
                visit_integral(integral, i, len(forms))

    # Now perform some checks on what should be done
    from dune.codegen.sumfact.vectorization import decide_vectorization_strategy
    logger.debug('generate_kernel: decide_vectorization_strategy')
    decide_vectorization_strategy()

    # Delete the cache contents and do the real thing!
    logger.debug('generate_kernel: visit_integrals (no dry run)')
    from dune.codegen.generation import delete_cache_items
    delete_cache_items("kernel_default")
    for i, form in enumerate(forms):
        for integral in form:
            visit_integral(integral, i, len(forms))

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

    return knl


def control_generate_kernels_per_integral(forms):
    """For the control problem forms will have one form for every
    measure. Every form will only contain integrals of one type.

    """
    yield generate_kernel(forms)
