""" Match FMA in expressions! """

from dune.codegen.loopy.symbolic import FusedMultiplyAdd as FMA
from loopy.symbolic import SubstitutionMapper

import loopy as lp
import pymbolic.primitives as prim


class FMASubstitutionMapper(SubstitutionMapper):
    def map_sum(self, expr):
        if len(expr.children) == 2:
            c1, c2 = expr.children
            if isinstance(c1, prim.Product) and len(c1.children) == 2:
                return FMA(self.rec(c1.children[0]), self.rec(c1.children[1]), self.rec(c2))
            if isinstance(c2, prim.Product) and len(c2.children) == 2:
                return FMA(self.rec(c2.children[0]), self.rec(c2.children[1]), self.rec(c1))
        return SubstitutionMapper.map_sum(self, expr)


def substitute_fma(expr):
    return FMASubstitutionMapper(lambda x: x)(expr)


def match_fused_multiply_add(knl):
    new_insns = []

    for insn in knl.instructions:
        if isinstance(insn, lp.Assignment):
            new_insns.append(insn.copy(expression=substitute_fma(insn.expression)))
        else:
            new_insns.append(insn)

    return knl.copy(instructions=new_insns)
