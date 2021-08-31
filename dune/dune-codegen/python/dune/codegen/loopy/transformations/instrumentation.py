""" Add instrumentation instructions to a kernel """

from dune.codegen.generation import (dump_accumulate_timer,
                                     register_liwkid_timer,
                                     post_include,
                                     )
from dune.codegen.options import get_option
from dune.codegen.pdelab.driver.timings import start_region_timer_instruction, stop_region_timer_instruction

import loopy as lp


def _intersect(a):
    """ Return intersection of a given tuple of frozensets. Also works for empty tuple """
    if len(a) == 0:
        return frozenset()
    return frozenset.intersection(*a)


def _union(a):
    """ Return union of a given tuple of frozensets. Also works for empty tuple """
    if len(a) == 0:
        return frozenset()
    return frozenset.union(*a)


def add_instrumentation(knl, match, identifier, level, filetag='operatorfile', operator=False, depends_on=frozenset()):
    """ Transform loopy kernel to contain instrumentation code

    Arguments:
    knl : The loopy kernel, follows the loopy transformation convention
    match : A loopy match object or a string (interpreted as instruction ID or tag) to describe
            which instructions should be wrapped in an instrumentation block.
    identifier : The name of the counter to start and stop
    level : The instrumentation level this measurement is defined at
    filetag : The tag of the file that should contain the counter definitions
    depends_on: Additional dependencies to add to the start instruction. This is used to correct
                currently wrong behaviour of the transformation in cases where a lot of structure
                of the instrumentation is known a priori.
    """
    # If the instrumentation level is not high enough, this is a no-op
    if level > get_option("instrumentation_level"):
        return knl

    # If a string was given for match, heuristically make it a match object
    if isinstance(match, str):
        match = lp.match.Or((lp.match.Id(match), lp.match.Tagged(match)))

    # Find the instructions to wrap in instrumentation
    insns = lp.find_instructions(knl, match)
    rewritten_insns = []

    # If the match is empty, this is also no op
    if not insns:
        return knl

    # Determine the iname nesting of the timing block
    insn_inames = _intersect(tuple(i.within_inames for i in insns))
    other_inames = _union(tuple(i.within_inames for i in lp.find_instructions(knl, lp.match.Not(match))))
    within = _intersect((insn_inames, other_inames))
    uniontags = _intersect(tuple(i.tags for i in insns))

    # Get a unique identifer - note that the same timer could be started and stopped several times
    # within one kernel...
    ident = identifier
    if lp.find_instructions(knl, lp.match.Id("{}_start".format(identifier))):
        ident = "{}_".format(ident)

    # Define the start instruction and correct dependencies for it
    start_id = "{}_start".format(ident)
    start_depends = _union(tuple(i.depends_on for i in insns)).difference(frozenset(i.id for i in insns))
    start_insn = start_region_timer_instruction(identifier,
                                                id=start_id,
                                                within_inames=within,
                                                depends_on=depends_on.union(start_depends),
                                                boostable_into=frozenset(),
                                                tags=uniontags,)

    # Add dependencies on the timing instructions
    rewritten_insns.extend([i.copy(depends_on=i.depends_on.union(frozenset({start_id}))) for i in insns])

    # Define the stop instruction and correct dependencies for it
    stop_id = "{}_stop".format(ident)
    stop_insn = stop_region_timer_instruction(identifier,
                                              id=stop_id,
                                              within_inames=within,
                                              depends_on=frozenset(i.id for i in insns),
                                              boostable_into=frozenset(),
                                              tags=uniontags,
                                              )

    # Find all the instructions that should depend on stop
    dep_insns = filter(lambda i: _intersect((i.depends_on, frozenset(i.id for i in insns))),
                       lp.find_instructions(knl, lp.match.Not(match))
                       )
    rewritten_insns.extend([i.copy(depends_on=i.depends_on.union(frozenset({stop_id}))) for i in dep_insns])

    # Trigger code generation on the file/operator level
    if get_option("use_likwid"):
        register_liwkid_timer(identifier)
    else:
        post_include('HP_DECLARE_TIMER({});'.format(identifier), filetag=filetag)
        dump_accumulate_timer(identifier)

    # Filter all the instructions which were untouched
    other_insns = list(filter(lambda i: i.id not in [j.id for j in rewritten_insns], knl.instructions))

    # Add all the modified instructions into the kernel object
    knl = knl.copy(instructions=rewritten_insns + other_insns + [start_insn, stop_insn])

    from loopy.kernel.creation import resolve_dependencies
    return resolve_dependencies(knl)
