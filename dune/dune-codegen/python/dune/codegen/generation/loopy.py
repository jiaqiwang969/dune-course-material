""" The loopy specific generators """
from __future__ import absolute_import

from dune.codegen.generation import (get_counter,
                                     generator_factory,
                                     no_caching,
                                     preamble,
                                     )
from dune.codegen.error import CodegenLoopyError

import loopy as lp
import numpy as np

iname = generator_factory(item_tags=("iname",), context_tags="kernel")
function_mangler = generator_factory(item_tags=("mangler",), context_tags="kernel")
silenced_warning = generator_factory(item_tags=("silenced_warning",), no_deco=True, context_tags="kernel")
kernel_cached = generator_factory(item_tags=("default_cached",), context_tags="kernel")


class DuneGlobalArg(lp.ArrayArg):
    allowed_extra_kwargs = lp.ArrayArg.allowed_extra_kwargs + ["managed"]


@generator_factory(item_tags=("argument", "globalarg"),
                   context_tags="kernel",
                   cache_key_generator=lambda n, **kw: n)
def globalarg(name, shape=lp.auto, managed=True, **kw):
    if isinstance(shape, str):
        shape = (shape,)
    from dune.codegen.loopy.target import dtype_floatingpoint
    dtype = kw.pop("dtype", dtype_floatingpoint())
    return DuneGlobalArg(name,
                         dtype=dtype,
                         shape=shape,
                         managed=managed,
                         address_space=lp.AddressSpace.GLOBAL,
                         **kw)


@generator_factory(item_tags=("argument", "constantarg"),
                   context_tags="kernel",
                   cache_key_generator=lambda n, **kw: n)
def constantarg(name, shape=None, **kw):
    if isinstance(shape, str):
        shape = (shape,)

    from dune.codegen.loopy.target import dtype_floatingpoint
    dtype = kw.pop("dtype", dtype_floatingpoint())
    return lp.GlobalArg(name, dtype=dtype, shape=shape, **kw)


@generator_factory(item_tags=("argument", "valuearg"),
                   context_tags="kernel",
                   cache_key_generator=lambda n, **kw: n)
def valuearg(name, **kw):
    from dune.codegen.loopy.target import dtype_floatingpoint
    dtype = kw.pop("dtype", dtype_floatingpoint())
    return lp.ValueArg(name, dtype=dtype, **kw)


@generator_factory(item_tags=("domain",), context_tags="kernel")
def domain(iname, shape):
    if isinstance(iname, tuple) and isinstance(shape, tuple):
        assert(len(iname) == len(shape))
        condition = ""
        for index, (i, s) in enumerate(zip(iname, shape)):
            if index > 0:
                condition += " and "
            else:
                condition += " "
            condition += "0<={}<{}".format(i, s)
        iname = ",".join(iname)
        return "{{ [{}] : {} }}".format(iname, condition)
    elif isinstance(iname, tuple):
        iname = ",".join(iname)
        if isinstance(shape, str):
            valuearg(shape)
    return "{{ [{0}] : 0<={0}<{1} }}".format(iname, shape)


def get_temporary_name():
    return 'expr_{}'.format(str(get_counter('__temporary').zfill(4)))


@generator_factory(item_tags=("temporary",),
                   context_tags="kernel",
                   cache_key_generator=lambda n, **kw: n)
def temporary_variable(name, **kwargs):
    from dune.codegen.loopy.temporary import DuneTemporaryVariable
    return DuneTemporaryVariable(name, scope=lp.temp_var_scope.PRIVATE, **kwargs)


# Now define generators for instructions. To ease dependency handling of instructions
# these generators are a bit more involved... We apply the following procedure:
# There is one generator that returns the unique id and forwards to a generator that
# actually adds the instruction. Hashing is done based on the code snippet.


@generator_factory(item_tags=("instruction", "cinstruction"),
                   context_tags="kernel",
                   cache_key_generator=lambda *a, **kw: kw['id'],
                   )
def c_instruction_impl(**kw):
    kw.setdefault('assignees', [])
    from pymbolic.primitives import Variable
    kw['assignees'] = frozenset(Variable(i) if isinstance(i, str) else i for i in kw['assignees'])
    inames = kw.pop('inames', kw.get('forced_iname_deps', []))

    return lp.CInstruction(inames, **kw)


@generator_factory(item_tags=("instruction", "exprinstruction"),
                   context_tags="kernel",
                   cache_key_generator=lambda *a, **kw: (kw['id']),
                   )
def expr_instruction_impl(**kw):
    if 'assignees' in kw:
        from pymbolic.primitives import Variable
        kw['assignees'] = frozenset(Variable(i) for i in kw['assignees'])
    return lp.ExpressionInstruction(**kw)


@generator_factory(item_tags=("instruction", "callinstruction"),
                   context_tags="kernel",
                   cache_key_generator=lambda *a, **kw: kw['expression'],
                   )
def call_instruction_impl(**kw):
    return lp.CallInstruction(**kw)


def _insn_cache_key(code=None, expression=None, **kwargs):
    if code is not None:
        return (code, kwargs.get('within_inames', None))
    if expression is not None:
        if 'assignees' in kwargs:
            return (kwargs['assignees'], expression)
        if 'assignee' in kwargs:
            return (kwargs['assignee'], expression)
    raise ValueError("Error caching instruction, missing information about assignee")


@generator_factory(item_tags=("insn_id",),
                   context_tags="kernel",
                   cache_key_generator=_insn_cache_key)
def instruction(code=None, expression=None, **kwargs):
    assert (code is not None) or (expression is not None)
    assert not ((code is not None) and (expression is not None))

    # Get an ID for this instruction
    id = kwargs.pop("id", 'insn_{}'.format(str(get_counter('__insn_id')).zfill(4)))

    # Now create the actual instruction
    if code:
        c_instruction_impl(id=id, code=code, **kwargs)
    if expression is not None:
        if 'assignees' in kwargs and len(kwargs['assignees']) == 0:
            call_instruction_impl(id=id, expression=expression, **kwargs)
        else:
            if 'assignees' in kwargs:
                assert 'assignee' not in kwargs
                kwargs['assignee'] = kwargs['assignees']
            expr_instruction_impl(id=id, expression=expression, **kwargs)

    # return the ID, as it is the only useful information to the user
    return id


@generator_factory(item_tags=("instruction",),
                   context_tags="kernel",
                   cache_key_generator=lambda **kw: kw['id'])
def noop_instruction(**kwargs):
    return lp.NoOpInstruction(**kwargs)


@generator_factory(item_tags=("transformation",),
                   context_tags="kernel",
                   cache_key_generator=no_caching,
                   )
def transform(trafo, *args, **kwargs):
    return (trafo, args, kwargs)


@generator_factory(item_tags=("instruction", "barrier"),
                   context_tags="kernel",
                   cache_key_generator=lambda **kw: kw['id'])
def _barrier(**kwargs):
    return lp.BarrierInstruction(**kwargs)


def barrier(**kwargs):
    assert 'id' not in kwargs
    name = 'barrier_{}'.format(get_counter('barrier'))
    _barrier(id=name, **kwargs)
    return name


def loopy_class_member(name, classtag=None, potentially_vectorized=False, **kwargs):
    """ A class member is based on loopy! It is an
    * temporary variable of the constructor kernel
    * A globalarg of the requesting kernel (to make things pass)
    """
    assert classtag
    assert "base_storage" not in kwargs

    if potentially_vectorized:
        base = "{}_base".format(name)
        kwargs["base_storage"] = base

    # Check if this is vectorized, if so, change name to vec
    dim_tags = kwargs.get("dim_tags", "")
    if dim_tags and dim_tags.split(',')[-1] == "vec":
        name = "{}_vec".format(name)

    temporary_variable(name, kernel=classtag, **kwargs)
    silenced_warning("read_no_write({})".format(name), kernel=classtag)

    kwargs.pop("decl_method", None)
    kwargs.pop("base_storage", None)
    # TODO I guess some filtering has to be applied here.
    globalarg(name, **kwargs)

    return name


@generator_factory(item_tags=("substrule",), context_tags="kernel")
def subst_rule(name, args, expr):
    return lp.SubstitutionRule(name, args, expr)
