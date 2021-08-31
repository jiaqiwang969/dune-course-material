from __future__ import absolute_import
from dune.codegen.generation import get_global_context_value
from pymbolic.interop.sympy import SympyToPymbolicMapper, PymbolicToSympyMapper
from functools import partial

import pymbolic.primitives as prim
import loopy as lp
import sympy as sp


class MyPymbolicToSympyMapper(PymbolicToSympyMapper):
    def map_if(self, expr):
        cond = self.rec(expr.condition)
        return sp.Piecewise((self.rec(expr.then), cond),
                            (self.rec(expr.else_), sp.Not(cond))
                            )

    def map_comparison(self, expr):
        left = self.rec(expr.left)
        right = self.rec(expr.right)
        if expr.operator == "==":
            return sp.Equality(left, right)
        elif expr.operator == "!=":
            return sp.Unequality(left, right)
        elif expr.operator == "<":
            return sp.StrictLessThan(left, right)
        elif expr.operator == ">":
            return sp.StrictGreaterThan(left, right)
        elif expr.operator == "<=":
            return sp.LessThan(left, right)
        elif expr.operator == ">=":
            return sp.GreaterThan(left, right)
        else:
            raise NotImplementedError("Cannot understand operator {}".format(expr.operator))

    def map_subscript(self, expr):
        return sp.tensor.indexed.Indexed(self.rec(expr.aggregate),
                                         *tuple(self.rec(i) for i in expr.index_tuple)
                                         )

    def map_tagged_variable(self, expr):
        return sp.Symbol("{}${}".format(expr.name, expr.tag))


class MySympyToPymbolicMapper(SympyToPymbolicMapper):
    def map_floor(self, expr):
        # Try finding patterns arising from FloorDiv
        assert isinstance(expr.args[0], sp.Mul)
        margs = expr.args[0].args
        if isinstance(margs[1], sp.Pow) and int(margs[1].args[1]) == -1:
            return prim.FloorDiv(self.rec(margs[0]), self.rec(margs[1].args[0]))
        elif isinstance(margs[0], sp.Rational) and margs[0].as_numer_denom()[0] == 1:
            return prim.FloorDiv(self.rec(margs[1]), self.rec(margs[0].as_numer_denom()[1]))
        else:
            raise NotImplementedError("Congratulations, sympy.floor showed you its deficits!")

    def map_Indexed(self, expr):
        return prim.Subscript(self.rec(expr.args[0].args[0]),
                              tuple(self.rec(i) for i in expr.args[1:])
                              )

    def map_Mod(self, expr):
        return prim.Remainder(self.rec(expr.args[0]), self.rec(expr.args[1]))

    def map_Symbol(self, expr):
        s = expr.name.split('$')
        r = prim.Variable(s[0])
        if len(s) == 1:
            return prim.Variable(s[0])
        else:
            return lp.symbolic.TaggedVariable(s[0], s[1])

    def map_Piecewise(self, expr):
        # We only handle piecewises with 2 arguments!
        assert len(expr.args) == 2
        # We only handle if/else cases
        assert expr.args[0][1] == sp.Not(expr.args[1][1])
        then = self.rec(expr.args[0][0])
        else_ = self.rec(expr.args[1][0])
        cond = self.rec(expr.args[0][1])
        return prim.If(cond, then, else_)

    def _comparison_operator(self, expr, operator=None):
        left = self.rec(expr.args[0])
        right = self.rec(expr.args[1])
        return prim.Comparison(left, operator, right)

    map_Equality = partial(_comparison_operator, operator="==")
    map_Unequality = partial(_comparison_operator, operator="!=")
    map_GreaterThan = partial(_comparison_operator, operator=">=")
    map_LessThan = partial(_comparison_operator, operator="<=")
    map_StrictGreaterThan = partial(_comparison_operator, operator=">")
    map_StrictLessThan = partial(_comparison_operator, operator="<")


def simplify_pymbolic_expression(e):
    if get_global_context_value("dry_run"):
        # If we are on the dry run, we skip this because our expression
        # may involve nodes that have no sympy equivalent (SumfactKernel...)
        return e
    else:
        forward = MyPymbolicToSympyMapper()
        backward = MySympyToPymbolicMapper()

        sympyexpr = forward(e)
        simplified = sp.simplify(sympyexpr)
        return backward(simplified)
