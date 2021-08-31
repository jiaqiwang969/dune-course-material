from loopy import (has_schedulable_iname_nesting,
                   get_iname_duplication_options,
                   duplicate_inames,
                   )


def blockstructured_iname_duplication(kernel):
    # If the given kernel is schedulable, nothing needs to be done.
    if has_schedulable_iname_nesting(kernel):
        return kernel

    # group inames with the same base name for duplication
    duplication_options = dict(get_iname_duplication_options(kernel))
    suffixes = ['x', 'y', 'z']
    for iname in duplication_options:
        if iname[-1] in suffixes:
            dup_kernel = kernel
            base = iname[:-1]
            for s in suffixes:
                if base + s in duplication_options:
                    dup_kernel = duplicate_inames(dup_kernel, base + s, duplication_options[base + s])
            if has_schedulable_iname_nesting(dup_kernel):
                return dup_kernel

    raise NotImplementedError("Your kernel needs multiple iname duplications! No generic algorithm implemented for that yet! (#39)")
