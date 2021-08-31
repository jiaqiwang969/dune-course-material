import re
import logging

import loopy as lp
import pymbolic.primitives as prim
import islpy as isl

from dune.codegen.generation import (get_counted_variable,
                                     get_global_context_value,
                                     )
from dune.codegen.loopy.transformations.remove_reductions import remove_all_reductions, remove_reduction
from dune.codegen.options import get_form_option, get_option
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.error import CodegenAutotuneError
from dune.codegen.sumfact.autotune import autotune_realization


def _current_iname_order(current_inames, new_iname_order):
    """Sort the inames for this contraction according to new_iname order"""
    current_iname_order = []
    for i in new_iname_order:
        for j in current_inames:
            if i in j:
                current_iname_order.append(j)
    return current_iname_order


def _get_inames_of_reduction(instr, iname_permutation):
    # Check which loops are inside the reduction loop
    reduction_index = iname_permutation[-1]
    within_reduction = tuple(i > reduction_index for i in iname_permutation)

    # Basename of inner inames
    dim = world_dimension()
    inner_inames_base = []
    for index, within in enumerate(within_reduction):
        if within:
            inner_inames_base.append('sf_out_inames_{}'.format(dim - 1 - index))

    # Name of inner inames and outer inames
    inner_inames = []
    outer_inames = []
    vec_inames = []
    for i in [iname for iname in instr.within_inames]:
        for j in inner_inames_base:
            if j in i:
                inner_inames.append(i)
        if 'sf_vec' in i:
            vec_inames.append(i)
        elif i not in inner_inames:
            outer_inames.append(i)

    # Reduction iname
    regex = re.compile('sf_red_([0-9]*)')
    reduction_index = set(regex.findall(str(instr)))
    if len(reduction_index) == 0:
        reduction_iname = None
    else:
        assert len(reduction_index) == 1
        reduction_index = reduction_index.pop()
        reduction_iname = 'sf_red_{}'.format(reduction_index)

    return outer_inames, reduction_iname, inner_inames, vec_inames


class FindReductionMapper(lp.symbolic.WalkMapper):
    def __init__(self):
        self.reductions = []

    def map_reduction(self, expr, **kwargs):
        self.reductions.append(expr)
        return lp.symbolic.WalkMapper.map_reduction(self, expr, **kwargs)


def _reorder_reduction_loops(kernel, match, iname_order):
    """Reorder loops in instructions containing one reduction

    In order to reorder the loops we need to manually do the accumulation in a
    temporary that is large enough to fit all the data created in loops inside
    the reduction loop.

    Parameters
    ----------
    kernel: loopy.kernel.LoopKernel
    match:
    iname_order: tuple of str
        prefered loop order for this instruction
    """
    instructions = lp.find_instructions(kernel, match)
    for instr in instructions:
        # Get reduction
        reduction = FindReductionMapper()
        reduction(instr.expression)
        assert len(reduction.reductions) == 1
        reduction = reduction.reductions[0]

        # Reduction iname, inner inames and vetcor inames
        assert len(reduction.inames) == 1
        reduction_iname = reduction.inames[0]
        assert set([reduction_iname]) == instr.reduction_inames()
        if reduction_iname not in iname_order:
            lp.prioritize_loops(kernel, iname_order)
            continue
        inner_inames = iname_order[iname_order.index(reduction_iname) + 1:]
        if len(inner_inames) == 0:
            lp.prioritize_loops(kernel, iname_order)
            continue
        # TODO: There should be a better way to do that
        vec_inames = [i for i in instr.within_inames if 'sf_vec' in i]
        assert len(vec_inames) < 2

        # {{{ Create new temporary variable

        # Create dim_tags
        dim_tags = ','.join(['f'] * len(inner_inames))
        vectorized = len(vec_inames) > 0
        if vectorized:
            assert len(vec_inames) == 1
            dim_tags = dim_tags + ',vec'

        # Create shape
        shape = tuple(kernel.get_constant_iname_length(i) for i in inner_inames + vec_inames)

        # Update temporary_variables of this kernel
        from dune.codegen.loopy.temporary import DuneTemporaryVariable
        accum_variable = get_counted_variable('accum_variable')
        from dune.codegen.loopy.target import dtype_floatingpoint
        dtype = lp.types.NumpyType(dtype_floatingpoint())
        var = {accum_variable: DuneTemporaryVariable(accum_variable,
                                                     dtype=dtype,
                                                     shape=shape,
                                                     dim_tags=dim_tags,
                                                     managed=True)}
        tv = kernel.temporary_variables.copy()
        tv.update(var)
        kernel = kernel.copy(temporary_variables=tv)

        # }}}

        # Set accumulation variable to zero
        accum_init_inames = tuple(prim.Variable(i) for i in inner_inames)
        if vectorized:
            accum_init_inames = accum_init_inames + (prim.Variable(vec_inames[0]),)
        assignee = prim.Subscript(prim.Variable(accum_variable,), accum_init_inames)
        accum_init_id = instr.id + '_accum_init'
        accum_init_instr = lp.Assignment(assignee,
                                         0,
                                         within_inames=instr.within_inames,
                                         id=accum_init_id,
                                         depends_on=instr.depends_on,
                                         tags=('accum_init',),
                                         )
        kernel = kernel.copy(instructions=kernel.instructions + [accum_init_instr])

        # Accumulate in temporary variable
        assignee = prim.Subscript(prim.Variable(accum_variable,), accum_init_inames)
        expression = prim.Sum((assignee, reduction.expr))
        within_inames = frozenset(tuple(instr.within_inames) + reduction.inames)
        accum_id = instr.id + '_accum'
        accum_instr = lp.Assignment(assignee,
                                    expression,
                                    within_inames=within_inames,
                                    id=accum_id,
                                    depends_on=frozenset([accum_init_id]),
                                    tags=('accum',),
                                    )
        kernel = kernel.copy(instructions=kernel.instructions + [accum_instr])

        # Replace reduction in insn with accumulation result
        def map_reduction(expr, rec):
            return assignee
        mapper = lp.symbolic.ReductionCallbackMapper(map_reduction)
        new_expression = mapper(instr.expression)
        assign_id = instr.id + '_assign'
        new_instr = instr.copy(expression=new_expression,
                               id=assign_id,
                               depends_on=frozenset(list(instr.depends_on) + [accum_id]))
        kernel = kernel.copy(instructions=kernel.instructions + [new_instr])

        # Fix dependencies and remove old instruction
        for i in kernel.instructions:
            if instr.id in i.depends_on:
                match = lp.match.Id(i.id)
                kernel = lp.add_dependency(kernel, match, assign_id)
        kernel = lp.remove_instructions(kernel, set([instr.id]))

        # Duplicate and reorder loops for accumulation
        ids = [accum_init_id, accum_id]
        duplicate_inames = tuple(inner_inames)
        for idx in ids:
            match = lp.match.Id(idx)
            kernel = lp.duplicate_inames(kernel, duplicate_inames, match)
            match_inames = tuple(lp.find_instructions(kernel, match)[0].within_inames)
            current_iname_order = _current_iname_order(match_inames, iname_order)
            kernel = lp.prioritize_loops(kernel, tuple(current_iname_order))

        # Reorder assignment loops
        kernel = lp.prioritize_loops(kernel, iname_order)
        return kernel


def _reorder_loops_in_tensor_contraction_direct(kernel, iname_permutation):
    """Reorder the loop nests of a tensor contraction accumulating directly in the data structure"""
    dim = world_dimension()

    # Nothing to do if permutation is identity
    if iname_permutation == tuple(range(dim + 1)):
        return kernel

    # Use names used in sum factorization kernel (without the index that distinguishes the different directions)
    default_iname_order = ['sf_out_inames_{}'.format(dim - 1 - i) for i in range(dim)] + ['sf_red']
    from dune.codegen.sumfact.permutation import permute_backward
    new_iname_order = permute_backward(default_iname_order, iname_permutation)

    for instr in kernel.instructions:
        # Inames used in this reduction
        outer_inames, reduction_iname, inner_inames, vec_inames = _get_inames_of_reduction(instr,
                                                                                           iname_permutation)
        if reduction_iname:
            current_inames = outer_inames + [reduction_iname] + inner_inames + vec_inames
        else:
            current_inames = outer_inames + inner_inames + vec_inames
        current_iname_order = _current_iname_order(current_inames,
                                                   new_iname_order)

        # We can directly use lp.prioritize_loops if
        # - The reduction is the innermost loop
        # - There is no reduction (eg reduced direction on faces)
        if iname_permutation[-1] == dim or reduction_iname is None:
            kernel = lp.prioritize_loops(kernel, tuple(current_iname_order))
            continue

        if isinstance(instr.expression, lp.symbolic.Reduction):
            # If the instruction is a reduction we can directly accumulate in the assignee
            assert set(inner_inames).issubset(set(i.name for i in instr.assignee.index_tuple))
            match = lp.match.Id(instr.id)
            kernel = remove_reduction(kernel, match)

            lp.prioritize_loops(kernel, current_iname_order)
            duplicate_inames = tuple(inner_inames)
            match = lp.match.Id(instr.id + '_set_zero')
            kernel = lp.duplicate_inames(kernel, duplicate_inames, match)
            match_inames = tuple(lp.find_instructions(kernel, match)[0].within_inames)
            set_zero_iname_order = _current_iname_order(match_inames, new_iname_order)
            lp.prioritize_loops(kernel, tuple(set_zero_iname_order))
        else:
            # In stage 3 this is usually not a reduction. In this case direct
            # accumulation is not possible and we accumulate in a temporay
            # variable instead
            match = lp.match.Id(instr.id)
            kernel = _reorder_reduction_loops(kernel, match, current_iname_order)

    return kernel


def _reorder_loops_in_tensor_contraction_accum(kernel, iname_permutation):
    """Reorder the loop nests of a tensor contraction using an accumulation variable"""
    dim = world_dimension()

    # Nothing to do if permutation is identity
    if iname_permutation == tuple(range(dim + 1)):
        return kernel

    # Use names used in sum factorization kernel (without the index that distinguishes the different directions)
    default_iname_order = ['sf_out_inames_{}'.format(dim - 1 - i) for i in range(dim)] + ['sf_red']
    from dune.codegen.sumfact.permutation import permute_backward
    new_iname_order = permute_backward(default_iname_order, iname_permutation)

    for instr in kernel.instructions:
        # Inames used in this reduction
        outer_inames, reduction_iname, inner_inames, vec_inames = _get_inames_of_reduction(instr,
                                                                                           iname_permutation)
        if reduction_iname:
            current_inames = outer_inames + [reduction_iname] + inner_inames + vec_inames
        else:
            current_inames = outer_inames + inner_inames + vec_inames
        current_iname_order = _current_iname_order(current_inames, new_iname_order)

        # We can directly use lp.prioritize_loops if:
        # - The reduction is the innermost loop
        # - There is no reduction (eg reduced direction on faces)
        if iname_permutation[-1] == dim or reduction_iname is None:
            kernel = lp.prioritize_loops(kernel, tuple(current_iname_order))
            continue

        match = lp.match.Id(instr.id)
        kernel = _reorder_reduction_loops(kernel, match, current_iname_order)

    return kernel


def reorder_loops_in_tensor_contraction(kernel, iname_permutation, accum_variable=True):
    """Change loop order in tensor contractions of sum factorization kernel

    Since there is a reduction involved this implies more than just reordering
    loops. There are two possibilities to handle the reduction:

    1) Generate an object of correct size for the accumulation and assign to
    the result data structure afterwards

    2) Make sure to set the correct entries of the result data structure to
    zero and accumulate inplace

    Parameters
    ----------
    kernel: loopy.kernel.LoopKernel
    iname_permutation: tuple of ints
        How to permute the loop inames. Should contain some permutation of the
        numbers 0 to dim+1
    accum_variable: bool
        If True use method 1 else use method 2 from above

    Notes
    -----
    Using einsum notation from numpy a contraction of a sum factorization
    kernel can be written as:

    - 3D: 'ij,jkl->kli'
    - 2D: 'ij,jk->ki'

    In the sum factorization kernel itself those inames are called:

    sf_out_inames_2_* : l
    sf_out_inames_1_* : k
    sf_out_inames_0_* : i
    sf_red_* : j

    where * represents the current direction (0,1,2 for 3D problems). The
    default order of the loops is

    (sf_out_iname_2_*, sf_out_iname_1_*, sf_out_iname_0_*, red_*)

    A permutation vector of (3,2,0,1) would mean that we do

    (sf_out_iname_0_*, red_*, sf_out_iname_1_*, sf_out_iname_2_*)

    instead.

    """
    if accum_variable:
        kernel = _reorder_loops_in_tensor_contraction_accum(kernel, iname_permutation)
        return kernel
    else:
        kernel = _reorder_loops_in_tensor_contraction_direct(kernel, iname_permutation)
        return kernel


def tensor_contraction_loop_order_generator(kernel):
    yield kernel, ['None']

    dim = world_dimension()
    identity = range(dim + 1)
    import itertools
    for permutation in itertools.permutations(identity):
        # Culling of stupid variant
        if permutation[0] == dim:
            continue

        new_kernel = reorder_loops_in_tensor_contraction(kernel, permutation, accum_variable=True)
        yield new_kernel, ['reorder_loops_in_tensor_contraction_{}_True'.format(permutation)]

        new_kernel = reorder_loops_in_tensor_contraction(kernel, permutation, accum_variable=False)
        yield new_kernel, ['reorder_loops_in_tensor_contraction_{}_False'.format(permutation)]


def simple_autotuner(kernel_generator, signature):
    kernel, transformations = next(kernel_generator)
    best_cost = autotune_realization(kernel=kernel, signature=signature, transformations=transformations)
    best_kernel = kernel
    best_transformations = transformations
    for kernel, transformations in kernel_generator:
        cost = autotune_realization(kernel=kernel, signature=signature, transformations=transformations)
        if cost < best_cost:
            best_cost = cost
            best_kernel = kernel
            best_transformations = transformations
    return best_kernel, best_transformations


def autotune_tensor_contraction_loop_order(kernel, signature):
    logger = logging.getLogger(__name__)

    assert get_option('autotune_google_benchmark')
    from dune.codegen.loopy.transformations.matchfma import match_fused_multiply_add
    kernel = match_fused_multiply_add(kernel)
    generator = tensor_contraction_loop_order_generator(kernel)
    kernel, transformations = simple_autotuner(generator, signature)
    logger.debug('autotute_tensor_contraction_loop_order - kernel {} transformations {}'.format(kernel.name, transformations))
    return kernel


def sumfact_performance_transformations(kernel, signature):
    if get_form_option('sumfact_performance_transformations'):
        assert not get_form_option('sumfact_performance_transformations_testrun')
        if kernel.name.startswith('sfimpl'):
            kernel = autotune_tensor_contraction_loop_order(kernel, signature)

    # Testing performance transformations
    elif get_form_option('sumfact_performance_transformations_testrun'):
        assert not get_form_option('sumfact_performance_transformations')
        if kernel.name.startswith('sfimpl'):
            dim = world_dimension()
            testcase = get_form_option('sumfact_performance_transformations_testrun')
            if dim == 2:
                testrun_dict = {
                    1: [(reorder_loops_in_tensor_contraction, ((0, 2, 1), True))],
                    2: [(reorder_loops_in_tensor_contraction, ((0, 2, 1), False))],
                    3: [(reorder_loops_in_tensor_contraction, ((2, 0, 1), True))],
                    4: [(reorder_loops_in_tensor_contraction, ((2, 0, 1), False))],
                }
                for trafo, arguments in testrun_dict[testcase]:
                    kernel = trafo(kernel, *arguments)
            else:
                testrun_dict = {
                    1: [(reorder_loops_in_tensor_contraction, ((3, 2, 0, 1), True))],
                    2: [(reorder_loops_in_tensor_contraction, ((3, 2, 0, 1), False))],
                    3: [(reorder_loops_in_tensor_contraction, ((2, 0, 1, 3), True))],
                    4: [(reorder_loops_in_tensor_contraction, ((2, 0, 1, 3), False))],
                }
                for trafo, arguments in testrun_dict[testcase]:
                    kernel = trafo(kernel, *arguments)
    return kernel
