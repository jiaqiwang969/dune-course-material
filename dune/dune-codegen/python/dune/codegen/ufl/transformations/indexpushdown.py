from __future__ import absolute_import
from ufl.algorithms import MultiFunction
from dune.codegen.ufl.flatoperators import get_operands, construct_binary_operator
from dune.codegen.ufl.transformations import ufl_transformation

import ufl.classes as uc


class IndexPushDown(MultiFunction):
    def expr(self, o):
        return self.reuse_if_untouched(o, *tuple(self(op) for op in o.ufl_operands))

    def indexed(self, o):
        expr, idx = o.ufl_operands
        if isinstance(expr, uc.Sum):
            terms = [uc.Indexed(self(term), idx) for term in get_operands(expr)]
            return construct_binary_operator(terms, uc.Sum)
        elif isinstance(expr, uc.Conditional):
            return uc.Conditional(self(expr.ufl_operands[0]),
                                  self(uc.Indexed(expr.ufl_operands[1], idx)),
                                  self(uc.Indexed(expr.ufl_operands[2], idx))
                                  )
        else:
            # This is a normal indexed, we treat it as any other.
            return self.expr(o)


@ufl_transformation(name="index_pushdown")
def pushdown_indexed(e):
    """
    Removes the following antipatterns from UFL expressions:
    * (a+b)[i] -> a[i] + b[i]
    * (a ? b : c)[i] -> a ? b[i] : c[i]

    If similar antipatterns arise with further nodes,
    add the corresponding handlers here.
    """
    return IndexPushDown()(e)
