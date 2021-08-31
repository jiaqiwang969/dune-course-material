import loopy as lp

import pymbolic.primitives as prim


def remove_reduction(knl, match):
    """Removes all matching reductions and do direct accumulation in assignee instead"""

    # Find reductions
    for instr in lp.find_instructions(knl, match):
        if isinstance(instr.expression, lp.symbolic.Reduction):
            instructions = []

            # Dependencies
            depends_on = instr.depends_on
            depending = []
            for i in knl.instructions:
                if instr.id in i.depends_on:
                    depending.append(i.id)

            # Remove the instruction from the kernel
            knl = lp.remove_instructions(knl, set([instr.id]))

            # Add instruction that sets assignee to zero
            id_zero = instr.id + '_set_zero'
            instructions.append(lp.Assignment(instr.assignee,
                                              0,
                                              within_inames=instr.within_inames,
                                              id=id_zero,
                                              tags=('set_zero',)
                                              ))

            # Add instruction that accumulates directly in assignee
            assignee = instr.assignee
            expression = prim.Sum((assignee, instr.expression.expr))
            within_inames = frozenset(tuple(instr.within_inames) + instr.expression.inames)
            id_accum = instr.id + '_accum'
            instructions.append(lp.Assignment(assignee,
                                              expression,
                                              within_inames=within_inames,
                                              id=id_accum,
                                              depends_on=frozenset((id_zero,) + tuple(depends_on)),
                                              tags=('assignment',)))

            knl = knl.copy(instructions=knl.instructions + instructions)

            # Restore dependencies
            for dep in depending:
                match = lp.match.Id(dep)
                knl = lp.add_dependency(knl, match, id_accum)
    return knl


def remove_all_reductions(knl):
    """Remove all reductions from loopy kernel

    This removes all reductions by instead setting the assignee to zero and
    directly accumulating in the assignee.
    """
    # Find ids of all reductions
    ids = []
    for instr in knl.instructions:
        if isinstance(instr.expression, lp.symbolic.Reduction):
            ids.append(instr.id)

    # Remove reductions
    for id in ids:
        match = lp.match.Id(id)
        knl = remove_reduction(knl, match)

    return knl
