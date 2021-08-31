""" Derive block preconditioners from residual forms """

from dune.codegen.ufl.modified_terminals import Restriction

from ufl.algorithms import MultiFunction
from ufl.algorithms.map_integrands import map_integrands

import ufl.classes as uc
import itertools


class OffDiagonalBlockSwitcher(MultiFunction):
    def __init__(self, restrictions):
        self.restrictions = restrictions
        self.res = Restriction.NONE
        MultiFunction.__init__(self)

    def expr(self, o):
        return self.reuse_if_untouched(o, *tuple(self(op) for op in o.ufl_operands))

    def positive_restricted(self, o):
        self.res = Restriction.POSITIVE
        ret = self(o.ufl_operands[0])
        self.res = Restriction.NONE
        if isinstance(ret, uc.Zero):
            return ret
        else:
            return o

    def negative_restricted(self, o):
        self.res = Restriction.NEGATIVE
        ret = self(o.ufl_operands[0])
        self.res = Restriction.NONE
        if isinstance(ret, uc.Zero):
            return ret
        else:
            return o

    def reference_value(self, o):
        ret = self(o.ufl_operands[0])
        if isinstance(ret, uc.Zero):
            return ret
        else:
            return o

    def argument(self, o):
        if self.res == self.restrictions[o.number()]:
            return o
        else:
            return uc.Zero(shape=o.ufl_shape,
                           free_indices=o.ufl_free_indices,
                           index_dimensions=o.ufl_index_dimensions)


def list_restriction_tuples(diagonal):
    if diagonal:
        yield (Restriction.NONE, Restriction.NONE)
        yield (Restriction.POSITIVE, Restriction.POSITIVE)
        return

    res = (Restriction.POSITIVE, Restriction.NEGATIVE)
    amount = 1 if diagonal else 2

    for rtup in itertools.product(res, res):
        if len(set(rtup)) == amount:
            yield rtup


def _block_jacobian(form, diagonal=True):
    assert(len(form.arguments()) == 2)

    forms = []
    for rtup in list_restriction_tuples(diagonal):
        forms.append(map_integrands(OffDiagonalBlockSwitcher(rtup), form))

    return sum(forms)


def diagonal_block_jacobian(form):
    return _block_jacobian(form)


def offdiagonal_block_jacobian(form):
    return _block_jacobian(form, False)
