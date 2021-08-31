import numpy as np

from dune.codegen.generation import post_include

from dune.codegen.generation.loopy import DuneGlobalArg
from dune.codegen.loopy.temporary import DuneTemporaryVariable
from dune.codegen.loopy.vcl import VCLTypeRegistry
from dune.codegen.generation import (include_file,
                                     retrieve_cache_functions,
                                     )
from dune.codegen.options import get_form_option, get_option
from dune.codegen.tools import round_to_multiple

from loopy.symbolic import Literal
from loopy.target import (TargetBase,
                          ASTBuilderBase,
                          DummyHostASTBuilder,
                          )
from loopy.target.c import CASTBuilder
from loopy.target.c.codegen.expression import ExpressionToCExpressionMapper, CExpressionToCodeMapper
from loopy.tools import is_integer
from loopy.types import NumpyType

from pymbolic.mapper.stringifier import PREC_NONE, PREC_BITWISE_AND, PREC_SHIFT
import pymbolic.primitives as prim

import pytools as pt

import cgen


def _type_to_op_counter_type(name):
    include_file("dune/opcounter/opcounter.hh")
    return "OpCounter::OpCounter<{}>".format(name)


def dtype_floatingpoint():
    bits = get_option("precision_bits")
    if bits == 32:
        return np.float32
    elif bits == 64:
        return np.float64
    else:
        raise NotImplementedError("{}bit floating point type".format(bits))


def numpy_to_cpp_dtype(key):
    _registry = {'float32': 'float',
                 'int32': 'int',
                 'float64': 'double',
                 'string': 'std::string',
                 'str': 'std::string'}

    if get_option('opcounter'):
        _registry['float32'] = _type_to_op_counter_type('float')
        _registry['float64'] = _type_to_op_counter_type('double')

    return _registry[key]


def type_floatingpoint():
    dtype = dtype_floatingpoint()
    return numpy_to_cpp_dtype(NumpyType(dtype).dtype.name)


def type_context_floatingpoint():
    return {np.float32: 'f', np.float64: 'd'}.get(dtype_floatingpoint())


class DuneExpressionToCExpressionMapper(ExpressionToCExpressionMapper):
    def map_subscript(self, expr, type_context):
        arr = self.find_array(expr)
        if isinstance(arr, (DuneTemporaryVariable, DuneGlobalArg)) and not arr.managed:
            # If there is but one index, we do not need to handle this
            if isinstance(expr.index, (prim.Variable, int)):
                return expr

            # Else, we construct a nested Subscript chain
            ret = expr.aggregate
            for i in expr.index:
                ret = prim.Subscript(ret, i)
            return ret
        else:
            return ExpressionToCExpressionMapper.map_subscript(self, expr, type_context)

    def map_floor_div(self, expr, enclosing_prec):
        # Loopy generates floor divs via a macro int_floor_div_pos_b
        # I have no idea why it does this and would like to generate
        # operator/ instead. At some point, I should ask Andreas about
        # the intention of that macro. Returning expr will pass this into
        # the CExpressionToCodeMapper as is => operator/.
        return expr

    def map_constant(self, expr, type_context):
        # We correct the type context to force all floating point literals to be of
        # the type that we use throughout the computation.
        if type_context in ("f", "d"):
            type_context = type_context_floatingpoint()
        ret = ExpressionToCExpressionMapper.map_constant(self, expr, type_context)
        if get_option('opcounter'):
            if type_context in ("f", "d"):
                ret = Literal("{}({})".format(type_floatingpoint(), ret.s))
        return ret

    def map_fused_multiply_add(self, expr, type_context):
        if self.codegen_state.vectorization_info:
            include_file("dune/codegen/common/muladd_workarounds.hh", filetag="operatorfile")
            # If this is vectorized we call the VCL function mul_add
            return prim.Call(prim.Variable("mul_add"),
                             (self.rec(expr.mul_op1, type_context),
                              self.rec(expr.mul_op2, type_context),
                              self.rec(expr.add_op, type_context)))
        else:
            # Default implementation that discards the node in favor of the resp.
            # additions and multiplications.
            return self.rec(expr.mul_op1 * expr.mul_op2 + expr.add_op, type_context)

    def map_if(self, expr, type_context):
        if self.codegen_state.vectorization_info:
            return prim.Call(prim.Variable("select"),
                             (self.rec(expr.condition, type_context),
                              self.rec(expr.then, type_context),
                              self.rec(expr.else_, type_context),
                              ))
        else:
            return ExpressionToCExpressionMapper.map_if(self, expr, type_context)


class DuneCExpressionToCodeMapper(CExpressionToCodeMapper):
    def map_remainder(self, expr, enclosing_prec):
        n = expr.denominator

        # check whether n is a power of 2
        if isinstance(n, int) and n & n - 1 == 0:
            # Issue optimized code using bit masks
            from pymbolic.mapper.stringifier import PREC_PRODUCT
            x = self.rec(expr.numerator, PREC_PRODUCT)
            return "({} & {})".format(x, n - 1)
        else:
            return CExpressionToCodeMapper.map_remainder(self, expr, enclosing_prec)

    def map_bitwise_and(self, expr, enclosing_prec):
        return self.parenthesize_if_needed(
            self.join_rec(" & ", expr.children, PREC_BITWISE_AND),
            enclosing_prec, PREC_BITWISE_AND)

    def map_right_shift(self, expr, enclosing_prec):
        return self.parenthesize_if_needed(
            "{} >> {}".format(self.rec(expr.shiftee, PREC_SHIFT),
                              self.rec(expr.shift, PREC_SHIFT)),
            enclosing_prec, PREC_SHIFT)

    map_tagged_variable = CExpressionToCodeMapper.map_variable


class DuneASTBuilder(CASTBuilder):
    def function_manglers(self):
        return retrieve_cache_functions("mangler") + CASTBuilder.function_manglers(self)

    def get_expression_to_c_expression_mapper(self, codegen_state):
        return DuneExpressionToCExpressionMapper(codegen_state)

    def get_c_expression_to_code_mapper(self):
        return DuneCExpressionToCodeMapper()

    def get_temporary_decl(self, codegen_state, schedule_index, temp_var, decl_info):
        # If this is not a DuneTemporaryVariable, it was introduced by loopy
        # and it should be totally under loopys control: Call the base class implementation!
        if not (isinstance(temp_var, DuneTemporaryVariable) and temp_var.custom_declaration):
            return CASTBuilder.get_temporary_decl(self, codegen_state, schedule_index, temp_var, decl_info)

        if temp_var.custom_declaration:
            decl = temp_var.decl_method(temp_var.name, codegen_state.kernel, decl_info)
            if decl:
                return cgen.Line(decl)

    def add_vector_access(self, access_expr, index):
        # There is no generic way of implementing a vector access with VCL, as
        # it might be that the entire statement needs to be rewritten. Consider
        # the example of an assignment to a vector component. It is *not* of the
        # form 'x.0 = 2' but instead its 'x.insert(0, 2)'. It is currently not
        # clear to me how this can be done, so I avoid the situation entirely.
        raise NotImplementedError()

    def emit_barrier(self, kind, comment):
        post_include("#define BARRIER asm volatile(\"\": : :\"memory\")", filetag="operatorfile")
        return cgen.Line("BARRIER;")

    def get_temporary_decls(self, codegen_state, schedule_index):
        temps = codegen_state.kernel.temporary_variables.values()
        # Declare all the custom base storages
        ret = []
        for bs in set(t.custom_base_storage for t in temps if isinstance(t, DuneTemporaryVariable)) - set({None}):
            if bs in [a.name for a in codegen_state.kernel.args]:
                continue

            # Find the alignment bytes
            alignment = []
            size = []
            for t in temps:
                if isinstance(t, DuneTemporaryVariable) and t.custom_base_storage == bs:
                    # TODO Extract alignment from the temporaries after switching to loopy 2018.1
                    alignment.append(get_option("max_vector_width") // 8)
                    from pytools import product
                    size.append(product(t.shape))

            alignment = max(alignment)
            size = max(size)
            size = round_to_multiple(size, alignment)

            decl = "char {}[{}] __attribute__ ((aligned({})));".format(bs, size * 8, alignment)
            ret.append(cgen.Line(decl))

        if self.target.declare_temporaries:
            return ret + CASTBuilder.get_temporary_decls(self, codegen_state, schedule_index)
        else:
            return ret


class BlockstructuredDuneExpressionToCExpressionMapper(DuneExpressionToCExpressionMapper):
    def map_variable(self, expr, type_context):
        arg = self.kernel.arg_dict.get(expr.name)
        # allow the use of pointers
        if isinstance(arg, DuneGlobalArg) and expr.name.endswith('alias'):
            return prim.Variable(expr.name)
        else:
            return ExpressionToCExpressionMapper.map_variable(self, expr, type_context)


class BlockstructuredDuneASTBuilder(DuneASTBuilder):
    def get_expression_to_c_expression_mapper(self, codegen_state):
        return BlockstructuredDuneExpressionToCExpressionMapper(codegen_state)

    def add_vector_access(self, access_expr, index):
        # In the vectorized blockstructured case I need read access to an element of an vector
        return prim.Subscript(access_expr, index)


class DuneTarget(TargetBase):
    def __init__(self, declare_temporaries=True):
        # Set fortran_abi to allow reusing CASTBuilder for the moment
        self.fortran_abi = False
        self.declare_temporaries = declare_temporaries

    def split_kernel_at_global_barriers(self):
        return False

    def get_host_ast_builder(self):
        return DummyHostASTBuilder(self)

    def get_device_ast_builder(self):
        if get_form_option("blockstructured"):
            return BlockstructuredDuneASTBuilder(self)
        else:
            return DuneASTBuilder(self)

    def dtype_to_typename(self, dtype):
        if dtype.dtype.kind == "V":
            include_file("dune/codegen/common/vectorclass.hh", filetag="operatorfile")
            return VCLTypeRegistry.names[dtype.dtype]
        else:
            return numpy_to_cpp_dtype(dtype.dtype.name)

    def is_vector_dtype(self, dtype):
        return dtype.dtype.kind == "V"

    def vector_dtype(self, base, count):
        return NumpyType(VCLTypeRegistry.types[base.numpy_dtype, count],
                         target=self)
