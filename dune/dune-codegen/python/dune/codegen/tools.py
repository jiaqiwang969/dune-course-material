""" Some grabbag tools """
from __future__ import absolute_import

import loopy as lp
import pymbolic.primitives as prim
import frozendict
import pytools


class ImmutableCuttingRecord(pytools.ImmutableRecord):
    """
    A record implementation that drops fields starting with an underscore
    from hash and equality computation
    """
    def __repr__(self):
        return "{}({})".format(type(self), ",".join(repr(getattr(self, f)) for f in self.__class__.fields if not f.startswith("_")))

    def __hash__(self):
        return hash((type(self),) + tuple(getattr(self, field) for field in self.__class__.fields if not field.startswith("_")))

    def __eq__(self, other):
        return type(self) == type(other) and all(getattr(self, field) == getattr(other, field) for field in self.__class__.fields if not field.startswith("_"))


def get_pymbolic_basename(expr):
    assert isinstance(expr, prim.Expression), "Type: {}, expr: {}".format(type(expr), expr)

    if isinstance(expr, prim.Variable):
        return expr.name

    if isinstance(expr, prim.Subscript):
        return get_pymbolic_basename(expr.aggregate)

    raise NotImplementedError("Cannot determine basename of {}".format(expr))


def get_pymbolic_indices(expr):
    if not isinstance(expr, prim.Subscript):
        return ()

    def ind(i):
        if isinstance(i, int):
            return (i,)
        elif isinstance(i, prim.Sum) or isinstance(i, prim.Product):
            return sum((ind(c) for c in i.children if isinstance(c, prim.Expression)), ())
        return (get_pymbolic_basename(i),)

    if not isinstance(expr.index, tuple):
        return (ind(expr.index),)

    return sum((ind(i) for i in expr.index), ())


def maybe_wrap_subscript(expr, indices):
    if indices is None:
        indices = ()
    if not isinstance(indices, tuple):
        indices = (indices,)
    if indices:
        if isinstance(expr, prim.Subscript):
            return prim.Subscript(expr.aggregate, expr.index + indices)
        else:
            return prim.Subscript(expr, indices)
    else:
        return expr


def get_pymbolic_tag(expr):
    assert isinstance(expr, prim.Expression)

    if isinstance(expr, lp.TaggedVariable):
        return expr.tag

    if isinstance(expr, prim.Variable):
        return None

    if isinstance(expr, prim.Subscript):
        return get_pymbolic_tag(expr.aggregate)

    raise NotImplementedError("Cannot determine tag on {}".format(expr))


def ceildiv(a, b):
    return -(-a // b)


def round_to_multiple(x, n):
    return n * ceildiv(x, n)


def add_to_frozendict(fd, valdict):
    t = dict(fd)
    t.update(valdict)
    return frozendict.frozendict(t)


def list_diff(l1, l2):
        l = []
        for item in l1:
            if item not in l2:
                l.append(item)
        return l


def get_leaf(element, index):
    """ return a leaf element if the given element is a MixedElement """
    leaf_element = element
    from ufl import MixedElement
    if isinstance(element, MixedElement):
        assert isinstance(index, int)
        leaf_element = element.extract_component(index)[1]

    return leaf_element


def remove_duplicates(iterable):
    """ Remove duplicates from an iterable while preserving the order """
    seen = set()
    for i in iterable:
        if i not in seen:
            yield i
            seen.add(i)
