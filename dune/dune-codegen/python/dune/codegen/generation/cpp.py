"""
Define some generators based on the caching mechanism that
are commonly needed for code generation
"""
from dune.codegen.options import get_option
from dune.codegen.generation import generator_factory
from dune.codegen.cgen.clazz import AccessModifier, BaseClass, ClassMember

import cgen


preamble = generator_factory(item_tags=("preamble",), counted=True, context_tags="kernel")
pre_include = generator_factory(item_tags=("file", "pre_include"), context_tags=("filetag",), no_deco=True)
post_include = generator_factory(item_tags=("file", "post_include"), context_tags=("filetag",), no_deco=True)
end_of_file = generator_factory(item_tags=("file", "end_of_file"), context_tags=("filetag",), no_deco=True)
class_member = generator_factory(item_tags=("member",), context_tags=("classtag",), on_store=lambda m: ClassMember(m), counted=True)
template_parameter = generator_factory(item_tags=("template_param",), context_tags=("classtag",), counted=True)
class_basename = generator_factory(item_tags=("basename",), context_tags=("classtag",))


@generator_factory(item_tags=("file", "include"), context_tags=("filetag",), counted=True)
def include_file(include, system=False):
    return cgen.Include(include, system=system)


@generator_factory(item_tags=("clazz", "initializer"), counted=True, context_tags=("classtag",), cache_key_generator=lambda o, p: o)
def initializer_list(obj, params):
    return "{}({})".format(obj, ", ".join(params))


@generator_factory(item_tags=("clazz", "baseclass"), context_tags=("classtag",), counted=True)
def base_class(baseclass, access=AccessModifier.PUBLIC, construction=[], classtag=None):
    if construction:
        initializer_list(baseclass, construction, classtag=classtag)

    return BaseClass(baseclass, inheritance=access)


@generator_factory(item_tags=("clazz", "constructor_param"), context_tags=("classtag",), counted=True)
def constructor_parameter(_type, name):
    return cgen.Value(_type, name)


@generator_factory(item_tags=("dump_timers",))
def dump_accumulate_timer(name):
    from dune.codegen.pdelab.localoperator import name_time_dumper_os
    os = name_time_dumper_os()
    # reset = name_time_dumper_reset()
    reset = 'false'

    code = "DUMP_TIMER({},{},{},{});".format(get_option("instrumentation_level"), name, os, reset)
    return code


@generator_factory(item_tags=("register_likwid_timers",))
def register_liwkid_timer(name):
    return "LIKWID_MARKER_REGISTER(\"{}\");".format(name)


@generator_factory(item_tags=("register_ssc_marks",))
def dump_ssc_marks(name):
    from dune.codegen.pdelab.driver.timings import get_region_marks
    return 'std::cout << "{}: " << {} << " <--> " << {} << std::endl;'.format(name,
                                                                              *get_region_marks(name, driver=False))
