from dune.codegen.blockstructured.tools import sub_element_inames, name_accumulation_alias
from dune.codegen.generation import accumulation_mixin, instruction, get_global_context_value
from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.pdelab.localoperator import determine_accumulation_space, GenericAccumulationMixin
from dune.codegen.pdelab.argument import name_accumulation_variable
from dune.codegen.pdelab.localoperator import boundary_predicates
from dune.codegen.generation.loopy import function_mangler
from dune.codegen.tools import get_pymbolic_basename
import loopy as lp
import pymbolic.primitives as prim

from loopy.match import Writes


@accumulation_mixin("blockstructured")
class BlockStructuredAccumulationMixin(GenericAccumulationMixin):
    def generate_accumulation_instruction(self, expr):
        if get_global_context_value("form_type") == "jacobian":
            return generate_accumulation_instruction(expr, self)
        else:
            return generate_accumulation_instruction_vectorized(expr, self)


@function_mangler
def residual_weight_mangler(knl, func, arg_dtypes):
    if isinstance(func, str) and func.endswith('.weight'):
        return lp.CallMangleInfo(func, (lp.types.NumpyType(dtype_floatingpoint()),), ())


def blockstructured_boundary_predicated(measure, subdomain_id):
    predicates = []

    if subdomain_id not in ['everywhere', 'otherwise']:
        subelem_inames = sub_element_inames()

        from dune.codegen.ufl.modified_terminals import Restriction
        from dune.codegen.blockstructured.geometry import name_face_id
        face_id = name_face_id(Restriction.POSITIVE)

        def face_id_equals(id):
            return prim.Comparison(prim.Variable(face_id), "==", id)

        def iname_equals(iname, i):
            return prim.Comparison(prim.Variable(iname), "==", i)

        k = get_form_option("number_of_blocks")

        if world_dimension() >= 2:
            predicates.append(prim.If(face_id_equals(0), iname_equals(subelem_inames[0], 0), True))
            predicates.append(prim.If(face_id_equals(1), iname_equals(subelem_inames[0], k - 1), True))
            predicates.append(prim.If(face_id_equals(2), iname_equals(subelem_inames[1], 0), True))
            predicates.append(prim.If(face_id_equals(3), iname_equals(subelem_inames[1], k - 1), True))
        if world_dimension() == 3:
            predicates.append(prim.If(face_id_equals(4), iname_equals(subelem_inames[2], 0), True))
            predicates.append(prim.If(face_id_equals(5), iname_equals(subelem_inames[2], k - 1), True))
    return frozenset(predicates)


def generate_accumulation_instruction(expr, visitor):
    # Collect the lfs and lfs indices for the accumulate call
    test_lfs = determine_accumulation_space(visitor.test_info, 0)
    # In the jacobian case, also determine the space for the ansatz space
    ansatz_lfs = determine_accumulation_space(visitor.trial_info, 1)

    # Collect the lfs and lfs indices for the accumulate call
    accumvar = name_accumulation_variable(test_lfs.get_restriction() + ansatz_lfs.get_restriction())

    predicates = boundary_predicates(visitor.measure, visitor.subdomain_id)
    predicates = predicates.union(blockstructured_boundary_predicated(visitor.measure, visitor.subdomain_id))

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


def generate_accumulation_instruction_vectorized(expr, visitor):
    # Collect the lfs and lfs indices for the accumulate call
    test_lfs = determine_accumulation_space(visitor.test_info, 0)
    # In the jacobian case, also determine the space for the ansatz space
    ansatz_lfs = determine_accumulation_space(visitor.trial_info, 1)

    # Collect the lfs and lfs indices for the accumulate call
    accumvar = name_accumulation_variable(test_lfs.get_restriction() + ansatz_lfs.get_restriction())
    accumvar_alias = name_accumulation_alias(accumvar, test_lfs)

    predicates = boundary_predicates(visitor.measure, visitor.subdomain_id)
    predicates = predicates.union(blockstructured_boundary_predicated(visitor.measure, visitor.subdomain_id))

    quad_inames = visitor.quadrature_inames()
    lfs_inames = visitor.test_info.inames
    if visitor.trial_info:
        lfs_inames = lfs_inames + visitor.trial_info.inames

    assignee = prim.Subscript(prim.Variable(accumvar_alias),
                              tuple(prim.Variable(i) for i in sub_element_inames() + lfs_inames))

    expr_with_weight = prim.Product((expr, prim.Call(prim.Variable(accumvar + '.weight'), ())))
    accum_expr = prim.Sum((expr_with_weight, assignee))
    deps = lp.symbolic.DependencyMapper()(accum_expr)
    deps = frozenset({Writes(get_pymbolic_basename(d)) for d in deps})

    instruction(assignee=assignee,
                expression=accum_expr,
                forced_iname_deps=frozenset(lfs_inames).union(frozenset(quad_inames)),
                forced_iname_deps_is_final=True,
                predicates=predicates,
                tags=frozenset({'accum'}),
                depends_on=deps
                )
