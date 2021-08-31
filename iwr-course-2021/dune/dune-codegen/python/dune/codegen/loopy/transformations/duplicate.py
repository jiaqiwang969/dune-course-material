""" Iname duplication strategies to make kernels schedulable """
from loopy import (has_schedulable_iname_nesting,
                   get_iname_duplication_options,
                   duplicate_inames,
                   )


def heuristic_duplication(kernel):
    # If the given kernel is schedulable, nothing needs to be done.
    if has_schedulable_iname_nesting(kernel):
        return kernel

    # List all duplication options and return the transformed
    # kernel if one such duplication transformation was enough to solve the problem.
    for iname, within in get_iname_duplication_options(kernel):
        dup_kernel = duplicate_inames(kernel, iname, within)
        if has_schedulable_iname_nesting(dup_kernel):
            return dup_kernel

    raise NotImplementedError("Your kernel needs multiple iname duplications! No generic algorithm implemented for that yet! (#39)")
