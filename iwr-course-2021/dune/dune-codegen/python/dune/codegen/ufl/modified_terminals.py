""" A module mimicking some functionality of uflacs' modified terminals """

from ufl.algorithms import MultiFunction
from ufl.classes import MultiIndex
from pytools import Record

import ufl.classes as uc


class Restriction:
    NONE = 0
    POSITIVE = 1
    NEGATIVE = 2


class ModifiedArgument(Record):
    def __init__(self,
                 expr=None,
                 argexpr=None,
                 grad=False,
                 index=None,
                 reference_grad=False,
                 restriction=Restriction.NONE,
                 tree_path=MultiIndex(()),
                 reference=False,
                 ):
        Record.__init__(self,
                        expr=expr,
                        argexpr=argexpr,
                        grad=grad,
                        index=index,
                        reference_grad=reference_grad,
                        restriction=restriction,
                        tree_path=tree_path,
                        reference=reference,
                        )


class ModifiedTerminalTracker(MultiFunction):
    """ A multifunction base that defines handler for
    grad, reference_grad, positive_restricted and negative_restricted.
    The appearance of those classes changes the internal state of the MF.
    """

    call = MultiFunction.__call__

    def __init__(self):
        MultiFunction.__init__(self)
        self.grad = False
        self.reference = True
        self.reference_grad = False
        self.restriction = Restriction.NONE
        self.tree_path = MultiIndex(())

    def positive_restricted(self, o):
        assert self.restriction == Restriction.NONE
        self.restriction = Restriction.POSITIVE
        ret = self.call(o.ufl_operands[0])
        self.restriction = Restriction.NONE
        return ret

    def negative_restricted(self, o):
        assert self.restriction == Restriction.NONE
        self.restriction = Restriction.NEGATIVE
        ret = self.call(o.ufl_operands[0])
        self.restriction = Restriction.NONE
        return ret

    def grad(self, o):
        assert not self.grad and not self.reference_grad
        self.grad = True
        ret = self.call(o.ufl_operands[0])
        self.grad = False
        return ret

    def reference_grad(self, o):
        assert not self.reference_grad and not self.grad
        self.reference_grad = True
        ret = self.call(o.ufl_operands[0])
        self.reference_grad = False
        return ret

    def reference_value(self, o):
        self.reference = True
        ret = self.call(o.ufl_operands[0])
        self.reference = False
        return ret


class ModifiedArgumentAnalysis(ModifiedTerminalTracker):
    def __init__(self, do_index=False):
        self.do_index = do_index
        self._index = None
        ModifiedTerminalTracker.__init__(self)

    def __call__(self, o):
        self.call_expr = o
        return self.call(o)

    def indexed(self, o):
        if all(isinstance(i, uc.FixedIndex) for i in o.ufl_operands[1]):
            self._index = o.ufl_operands[1]
        if self.do_index and all(isinstance(i, uc.Index) for i in o.ufl_operands[1]):
            self._index = o.ufl_operands[1]
        return self.call(o.ufl_operands[0])

    def form_argument(self, o):
        return ModifiedArgument(expr=self.call_expr,
                                argexpr=o,
                                index=self._index,
                                restriction=self.restriction,
                                tree_path=self.tree_path,
                                grad=self.grad,
                                reference_grad=self.reference_grad,
                                reference=self.reference,
                                )


def analyse_modified_argument(expr, **kwargs):
    return ModifiedArgumentAnalysis(**kwargs)(expr)


class _ModifiedArgumentExtractor(MultiFunction):
    """ A multifunction that extracts and returns the set of modified arguments """

    def __call__(self, o, argnumber=None, coeffcount=None, do_index=False, do_gradient=True):
        self.argnumber = argnumber
        self.coeffcount = coeffcount
        self.do_index = do_index
        self.do_gradient = do_gradient
        self.modified_arguments = set()
        ret = self.call(o)
        if ret:
            # This indicates that this entire expression was a modified thing...
            self.modified_arguments.add(ret)
        return tuple(analyse_modified_argument(ma,
                                               do_index=self.do_index
                                               )
                     for ma in self.modified_arguments)

    def expr(self, o):
        for op in o.ufl_operands:
            ret = self.call(op)
            if ret:
                self.modified_arguments.add(ret)

    def pass_on(self, o):
        if self.call(o.ufl_operands[0]):
            return o

    def indexed(self, o):
        if all(isinstance(i, uc.FixedIndex) for i in o.ufl_operands[1]):
            return self.pass_on(o)
        if self.do_index and all(isinstance(i, uc.Index) for i in o.ufl_operands[1]):
            return self.pass_on(o)
        else:
            self.expr(o)

    def reference_grad(self, o):
        if self.do_gradient:
            return self.pass_on(o)
        else:
            self.expr(o)

    def grad(self, o):
        if self.do_gradient:
            return self.pass_on(o)
        else:
            self.expr(o)

    positive_restricted = pass_on
    negative_restricted = pass_on
    reference_value = pass_on

    def argument(self, o):
        if o.number() == self.argnumber:
            return o

    def coefficient(self, o):
        if o.count() == self.coeffcount:
            return o

    call = MultiFunction.__call__


def extract_modified_arguments(expr, **kwargs):
    return _ModifiedArgumentExtractor()(expr, **kwargs)
