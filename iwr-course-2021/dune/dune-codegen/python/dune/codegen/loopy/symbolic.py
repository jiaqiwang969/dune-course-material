""" Monkey patches for loopy.symbolic

Use this module to insert pymbolic nodes and the likes.
"""
from dune.codegen.error import CodegenError
from pymbolic.mapper.substitutor import make_subst_func
from pymbolic.mapper.constant_folder import CommutativeConstantFoldingMapper as ConstantFoldingMapperBase

import pymbolic
import loopy as lp
import pymbolic.primitives as prim
from pytools import memoize_method
from six.moves import intern


#
# Pymbolic nodes to insert into the symbolic language understood by loopy
#

class InplaceCallInstruction(lp.CallInstruction):
    fields = lp.CallInstruction.fields | {"inplace_assignees"}
    pymbolic_fields = lp.CallInstruction.pymbolic_fields | {"inplace_assignees"}

    def __init__(self, inplace_assignees, expression, assignees=(), **kwargs):
        super().__init__(assignees, expression, **kwargs)

        if not isinstance(inplace_assignees, tuple):
            raise CodegenError("'inplace_assignees' argument to InplaceCallInstruction "
                               "must be a tuple -- got '%s'" % type(assignees).__name__)

        self.inplace_assignees = inplace_assignees

    @memoize_method
    def assignee_var_names(self):
        from loopy.kernel.instruction import _get_assignee_var_name
        return tuple(_get_assignee_var_name(a) for a in self.inplace_assignees + self.assignees)

    def assignee_subscript_deps(self):
        from loopy.kernel.instruction import _get_assignee_subscript_deps
        return tuple(
            _get_assignee_subscript_deps(a)
            for a in self.inplace_assignees + self.assignees)

    def with_transformed_expressions(self, f, *args):
        return self.copy(
            inplace_assignees=f(self.inplace_assignees, *args),
            expression=f(self.expression, *args),
            assignees=f(self.assignees, *args),
            predicates=frozenset(
                f(pred, *args) for pred in self.predicates))


class FusedMultiplyAdd(prim.Expression):
    """ Represents an FMA operation """

    init_arg_names = ("mul_op1", "mul_op2", "add_op")

    def __init__(self, mul_op1, mul_op2, add_op):
        self.mul_op1 = mul_op1
        self.mul_op2 = mul_op2
        self.add_op = add_op

    def __getinitargs__(self):
        return (self.mul_op1, self.mul_op2, self.add_op)

    def make_stringifier(self, originating_stringifier=None):
        return lp.symbolic.StringifyMapper()

    mapper_method = intern("map_fused_multiply_add")


#
# Mapper methods to monkey patch into the visitor base classes!
#


def identity_map_sumfact_kernel(self, expr, *args):
    return expr


def walk_map_sumfact_kernel(self, expr, *args):
    self.visit(expr)


def stringify_map_sumfact_kernel(self, expr, *args):
    return str(expr)


def dependency_map_sumfact_kernel(self, expr):
    return set()


def needs_resolution(self, expr):
    raise CodegenError("SumfactKernel node is a placeholder and needs to be removed!")


def identity_map_fused_multiply_add(self, expr, *args):
    return FusedMultiplyAdd(self.rec(expr.mul_op1, *args),
                            self.rec(expr.mul_op2, *args),
                            self.rec(expr.add_op, *args),
                            )


def walk_map_fused_multiply_add(self, expr, *args):
    if not self.visit(expr, *args):
        return

    self.rec(expr.mul_op1, *args)
    self.rec(expr.mul_op2, *args)
    self.rec(expr.add_op, *args)

    self.post_visit(expr, *args)


def stringify_map_fused_multiply_add(self, expr, enclosing_prec):
    from pymbolic.mapper.stringifier import PREC_NONE
    return "fma(%s*%s+%s)" % (self.rec(expr.mul_op1, PREC_NONE),
                              self.rec(expr.mul_op2, PREC_NONE),
                              self.rec(expr.add_op, PREC_NONE))


def combine_map_fused_multiply_add(self, expr):
    return self.combine((self.rec(expr.mul_op1),
                         self.rec(expr.mul_op2),
                         self.rec(expr.add_op)
                         ))


def type_inference_fused_multiply_add(self, expr):
    return self.combine([self.rec(expr.mul_op1), self.rec(expr.mul_op2), self.rec(expr.add_op)])


def vectorizability_map_fused_multiply_add(self, expr):
    return all((self.rec(expr.mul_op1), self.rec(expr.mul_op2), self.rec(expr.add_op)))

#
# Do the actual monkey patching!!!
#

# SumfactKernel node
lp.symbolic.IdentityMapper.map_sumfact_kernel = identity_map_sumfact_kernel
lp.symbolic.SubstitutionMapper.map_sumfact_kernel = lp.symbolic.SubstitutionMapper.map_variable
lp.symbolic.WalkMapper.map_sumfact_kernel = walk_map_sumfact_kernel
lp.symbolic.StringifyMapper.map_sumfact_kernel = stringify_map_sumfact_kernel
lp.symbolic.DependencyMapper.map_sumfact_kernel = dependency_map_sumfact_kernel
lp.target.c.codegen.expression.ExpressionToCExpressionMapper.map_sumfact_kernel = needs_resolution
lp.type_inference.TypeInferenceMapper.map_sumfact_kernel = needs_resolution

# VectorizedSumfactKernel node
lp.symbolic.IdentityMapper.map_vectorized_sumfact_kernel = identity_map_sumfact_kernel
lp.symbolic.SubstitutionMapper.map_vectorized_sumfact_kernel = lp.symbolic.SubstitutionMapper.map_variable
lp.symbolic.WalkMapper.map_vectorized_sumfact_kernel = walk_map_sumfact_kernel
lp.symbolic.StringifyMapper.map_vectorized_sumfact_kernel = stringify_map_sumfact_kernel
lp.symbolic.DependencyMapper.map_vectorized_sumfact_kernel = dependency_map_sumfact_kernel
lp.target.c.codegen.expression.ExpressionToCExpressionMapper.map_vectorized_sumfact_kernel = needs_resolution
lp.type_inference.TypeInferenceMapper.map_vectorized_sumfact_kernel = needs_resolution

# FusedMultiplyAdd node
lp.symbolic.IdentityMapper.map_fused_multiply_add = identity_map_fused_multiply_add
lp.symbolic.SubstitutionMapper.map_fused_multiply_add = identity_map_fused_multiply_add
lp.symbolic.WalkMapper.map_fused_multiply_add = walk_map_fused_multiply_add
lp.symbolic.StringifyMapper.map_fused_multiply_add = stringify_map_fused_multiply_add
lp.symbolic.DependencyMapper.map_fused_multiply_add = combine_map_fused_multiply_add
lp.symbolic.CombineMapper.map_fused_multiply_add = combine_map_fused_multiply_add
lp.type_inference.TypeInferenceMapper.map_fused_multiply_add = type_inference_fused_multiply_add
lp.expression.VectorizabilityChecker.map_fused_multiply_add = vectorizability_map_fused_multiply_add
pymbolic.mapper.dependency.DependencyMapper.map_fused_multiply_add = combine_map_fused_multiply_add
pymbolic.mapper.dependency.DependencyMapper.map_reduction = lp.symbolic.DependencyMapper.map_reduction


#
# Some helper functions!
#


def substitute(expr, replacemap):
    """ A replacement for pymbolic.mapper.subsitutor.substitute which is aware of all
    monkey patches etc.
    """
    return lp.symbolic.SubstitutionMapper(make_subst_func(replacemap))(expr)
