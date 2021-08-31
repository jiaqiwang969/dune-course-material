"""
This module defines the main visitor algorithm transforming ufl expressions
to pymbolic and loopy.
"""
from dune.codegen.error import CodegenUFLError
from dune.codegen.generation import (get_global_context_value,
                                     domain,
                                     globalarg,
                                     valuearg,
                                     )
from dune.codegen.ufl.flatoperators import get_operands
from dune.codegen.ufl.modified_terminals import (ModifiedTerminalTracker,
                                                 Restriction,
                                                 )
from dune.codegen.tools import maybe_wrap_subscript
from dune.codegen.options import get_form_option
from loopy import Reduction

from pymbolic.primitives import (Call,
                                 Product,
                                 Quotient,
                                 Subscript,
                                 Sum,
                                 Variable,
                                 )

from ufl.algorithms import MultiFunction
from ufl.checks import is_cellwise_constant
from ufl import (VectorElement,
                 MixedElement,
                 TensorElement,
                 TensorProductElement,
                 )
from ufl.classes import (Coefficient,
                         FixedIndex,
                         IndexSum,
                         JacobianDeterminant,
                         )

from pytools import product as ptproduct
import pymbolic.primitives as prim
import numpy as np


class UFL2LoopyVisitor(ModifiedTerminalTracker):
    def __init__(self, measure, subdomain_id, **kwargs):
        self.measure = measure
        self.subdomain_id = subdomain_id

        # Call base class constructors
        super(UFL2LoopyVisitor, self).__init__()

    def __call__(self, o, do_predicates=False):
        self.current_info = None
        return self._call(o, do_predicates)

    def accumulate(self, o):
        for info in self.list_accumulation_infos(o):
            self.current_info = info
            expr = self._call(o, False)
            if expr != 0:
                if get_form_option("simplify"):
                    from dune.codegen.sympy import simplify_pymbolic_expression
                    expr = simplify_pymbolic_expression(expr)
                self.generate_accumulation_instruction(expr)

    def _call(self, o, do_predicates):
        # Reset state variables
        self.indexmap = {}
        self.indices = None
        self._indices_backup = []
        self.test_info = None
        self.trial_info = None
        self.inames = ()
        self.do_predicates = do_predicates

        return self.call(o)

    def call(self, o):
        # Allow downstream projects to provide custom nodes that provide their own visiting
        # implementation. To do so, inherit from the UFL node which is closest to what you need
        # and provide it with the following:
        # * a _ufl_expr_reconstruct_ method to avoid preprocessing discarding the node
        # * a visit method taking the visitor as the only argument
        if hasattr(o, "visit"):
            return o.visit(self)
        else:
            return MultiFunction.__call__(self, o)

    #
    # Form argument/coefficients handlers:
    # This is where the actual domain specific work happens
    #

    def argument(self, o):
        self.initialize_function_spaces(o)
        # Update the information on where to accumulate this
        info = self.get_accumulation_info(o)
        if o.number() == 0:
            if info != self.current_info[0]:
                self.indices = None
                return 0
            else:
                self.test_info = info
        elif o.number() == 1:
            if info != self.current_info[1]:
                self.indices = None
                return 0
            else:
                self.trial_info = info

        # Correct the restriction on boundary integrals
        restriction = self.restriction
        if self.measure == 'exterior_facet':
            restriction = Restriction.POSITIVE
        leaf_element = o.ufl_element()

        # Select the correct leaf element in the case of this being a mixed finite element
        if isinstance(o.ufl_element(), MixedElement):
            index = self.indices[0]
            assert isinstance(index, int)
            self.indices = self.indices[1:]
            if len(self.indices) == 0:
                self.indices = None

            # For the purpose of basis evaluation, we need to take the leaf element
            leaf_element = leaf_element.extract_component(index)[1]

        if self.grad:
            raise CodegenUFLError("Gradients should have been transformed to reference gradients!!!")

        if self.reference_grad:
            return self.implement_reference_gradient(leaf_element, restriction, o.number())
        else:
            return self.implement_basis(leaf_element, restriction, o.number())

    def coefficient(self, o):
        # Correct the restriction on boundary integrals
        restriction = self.restriction
        if self.measure == 'exterior_facet':
            restriction = Restriction.POSITIVE

        # count() == 2 is reserved for the time variable and treated in a different way
        if o.count() == 2:
            # The base class 'InstationaryLocalOperatorDefaultMethods' stores the time
            # and exports it through a getter method 'getTime'
            return prim.Call(prim.Variable("getTime"), ())

        else:
            self.initialize_function_spaces(o)

            index = None
            if isinstance(o.ufl_element(), MixedElement):
                index = self.indices[0]
                assert isinstance(index, int)
                self.indices = self.indices[1:]
                if len(self.indices) == 0:
                    self.indices = None

            if self.grad:
                raise CodegenUFLError("Gradients should have been transformed to reference gradients!")

            # Three cases:
            # - count() == 0: This represents the ansatz function
            # - count() == 1: This represents the coefficient function used in the jacobian apply method
            # - count() >= 2: Additional finite element function
            if self.reference_grad:
                if o.count() == 0:
                    return self.implement_trialfunction_gradient(o.ufl_element(), restriction, index)
                elif o.count() == 1:
                    return self.implement_apply_function_gradient(o.ufl_element(), restriction, index)
                else:
                    return self.implement_coefficient_function_gradient(o, restriction, index)
            else:
                if o.count() == 0:
                    return self.implement_trialfunction(o.ufl_element(), restriction, index)
                elif o.count() == 1:
                    return self.implement_apply_function(o.ufl_element(), restriction, index)
                else:
                    return self.implement_coefficient_function(o, restriction, index)

    def variable(self, o):
        return self.call(o.ufl_operands[0])

    #
    # Handlers for all indexing related stuff
    #

    def indexed(self, o):
        # Handle indices first to allow the aggregate handler to mangle in indices
        # This is necessary in some places where the locality of the tree transformation
        # is not given (easiest example: jacobian_inverse handler, complex example:
        # sum factorziation handler for trial function gradient)
        self._indices_backup.append(self.indices)
        self.indices = self.call(o.ufl_operands[1])

        # Handle the aggregate!
        aggr = self.call(o.ufl_operands[0])

        # self.indices being None means they are already handled during recursion!
        if self.indices is None:
            self.indices = self._indices_backup.pop()
            return aggr
        else:
            indices = self.indices
            self.indices = self._indices_backup.pop()
            return maybe_wrap_subscript(aggr, indices)

    def index_sum(self, o):
        # This implementation fully unrolls the given indexed sum.
        # This is done for a variety of reasons:
        # * It eases handling of the given loopy kernel in terms of schedulability
        # * The compiler would unroll these anyway
        # * It allows handling of arbitrarily bad nesting of ComponentTensor and
        #   ListTensor, which otherwise becomes a *nightmare*.
        index = o.ufl_operands[1][0]
        operands = []
        stack_indices = self.indices

        for i in range(o.dimension()):
            self.indices = stack_indices
            self.indexmap[index] = i
            operands.append(self.call(o.ufl_operands[0]))
            del self.indexmap[index]

        from pymbolic import flattened_sum
        return flattened_sum(tuple(operands))

    def _index_or_fixed_index(self, index):
        if isinstance(index, FixedIndex):
            return index._value
        else:
            if index in self.indexmap:
                return self.indexmap[index]
            else:
                raise CodegenUFLError("Index should have been unrolled!")

    def multi_index(self, o):
        return tuple(self._index_or_fixed_index(i) for i in o)

    def index(self, o):
        return self._index_or_fixed_index(o)

    def list_tensor(self, o):
        if all(isinstance(i, int) for i in self.indices):
            index = self.indices[0]
            self.indices = self.indices[1:]
            if len(self.indices) == 0:
                self.indices = None
            return self.call(o.ufl_operands[index])
        else:
            raise CodegenUFLError("Index should have been unrolled!")

    def component_tensor(self, o):
        assert len(self.indices) == len(o.ufl_operands[1])
        # Update the index mapping
        for i, ind in enumerate(o.ufl_operands[1]):
            self.indexmap[ind] = self.indexmap.get(self.indices[i], self.indices[i])

        self.indices = None
        ret = self.call(o.ufl_operands[0])

        for i, ind in enumerate(o.ufl_operands[1]):
            del self.indexmap[ind]

        return ret

    def identity(self, o):
        i, j = self.indices
        self.indices = None
        assert isinstance(i, int) and isinstance(j, int)
        return 1 if i == j else 0

    def inverse(self, o):
        from dune.codegen.pdelab.tensors import pymbolic_matrix_inverse
        return pymbolic_matrix_inverse(o, self)

    #
    # Handlers for arithmetic operators and functions
    # Those handlers would be valid in any code going from UFL to pymbolic
    #

    def product(self, o):
        ops = tuple(self.call(op) for op in o.ufl_operands)
        if all(isinstance(op, (int, float)) for op in ops):
            return ptproduct(ops)
        return prim.flattened_product(ops)

    def float_value(self, o):
        return o.value()

    def int_value(self, o):
        return o.value()

    def division(self, o):
        divisor = self.call(o.ufl_operands[1])
        if isinstance(divisor, (int, float)):
            return prim.Product((self.call(o.ufl_operands[0]), 1 / divisor))
        else:
            return prim.quotient(self.call(o.ufl_operands[0]), divisor)

    def sum(self, o):
        ops = tuple(self.call(op) for op in o.ufl_operands)
        if all(isinstance(op, (int, float)) for op in ops):
            return sum(ops)
        return prim.flattened_sum(ops)

    def zero(self, o):
        # UFL has Zeroes with shape. We ignore those indices.
        self.indices = None
        return 0.0

    def _evaluate_function(self, python_func, c_func, vals):
        assert isinstance(vals, tuple)
        if all(isinstance(v, (float, int)) for v in vals):
            return python_func(*vals)
        else:
            return prim.Call(prim.Variable(c_func), vals)

    def abs(self, o):
        if isinstance(o.ufl_operands[0], JacobianDeterminant):
            return self.call(o.ufl_operands[0])
        else:
            return self._evaluate_function(abs, "abs", (self.call(o.ufl_operands[0]),))

    def exp(self, o):
        return self._evaluate_function(np.exp, "exp", (self.call(o.ufl_operands[0]),))

    def sqrt(self, o):
        return self._evaluate_function(np.sqrt, "sqrt", (self.call(o.ufl_operands[0]),))

    def sin(self, o):
        return self._evaluate_function(np.sin, "sin", (self.call(o.ufl_operands[0]),))

    def cos(self, o):
        return self._evaluate_function(np.cos, "cos", (self.call(o.ufl_operands[0]),))

    def power(self, o):
        base = self.call(o.ufl_operands[0])
        exponent = self.call(o.ufl_operands[1])
        if isinstance(base, (float, int)) and isinstance(exponent, (float, int)):
            return base**exponent
        elif isinstance(exponent, int):
            return prim.Product((base,) * exponent)
        else:
            return prim.Power(base, exponent)

    def _minmax_impl(self, python_func, c_func, children):
        # Build the maximum of those that are constant
        constants = list(filter(lambda i: isinstance(i, (float, int)), children))
        children = set(filter(lambda i: not isinstance(i, (float, int)), children))

        if constants:
            if len(children) == 0:
                return python_func(constants)
            else:
                children.add(python_func(constants))

        # std::max/min takes but two arguments -> construct a chain!
        ret = children.pop()
        while children:
            # NB: There is a pymbolic node Max/Min, which we are intentionally
            # avoiding here, as the C++ nature is so much more like a function!
            ret = prim.Call(prim.Variable(c_func), (ret, children.pop()))

        return ret

    def max_value(self, o):
        return self._minmax_impl(max, "max", tuple(self.call(op) for op in o.ufl_operands))

    def min_value(self, o):
        return self._minmax_impl(min, "min", tuple(self.call(op) for op in o.ufl_operands))

    #
    # Handler for conditionals, use pymbolic base implementation
    #

    def conditional(self, o):
        cond = self.call(o.ufl_operands[0])

        # Try to evaluate the condition at code generation time
        try:
            evaluated = eval(str(cond))
        except:
            op1 = self.call(o.ufl_operands[1])
            op2 = self.call(o.ufl_operands[2])

            # This conditional might be redundant!
            if op1 == op2:
                return op1

            return prim.If(cond, op1, op2)

        # User code generation time evaluation
        if evaluated:
            return self.call(o.ufl_operands[1])
        else:
            return self.call(o.ufl_operands[2])

    def eq(self, o):
        return prim.Comparison(self.call(o.ufl_operands[0]),
                               "==",
                               right=self.call(o.ufl_operands[1]))

    def ge(self, o):
        return prim.Comparison(self.call(o.ufl_operands[0]),
                               ">=",
                               right=self.call(o.ufl_operands[1]))

    def gt(self, o):
        return prim.Comparison(self.call(o.ufl_operands[0]),
                               ">",
                               right=self.call(o.ufl_operands[1]))

    def le(self, o):
        return prim.Comparison(self.call(o.ufl_operands[0]),
                               "<=",
                               right=self.call(o.ufl_operands[1]))

    def lt(self, o):
        return prim.Comparison(self.call(o.ufl_operands[0]),
                               "<",
                               right=self.call(o.ufl_operands[1]))

    def ne(self, o):
        return prim.Comparison(self.call(o.ufl_operands[0]),
                               "!=",
                               right=self.call(o.ufl_operands[1]))

    def and_condition(self, o):
        return prim.LogicalAnd((self.call(o.ufl_operands[0]), self.call(o.ufl_operands[1])))

    def or_condition(self, o):
        return prim.LogicalOr((self.call(o.ufl_operands[0]), self.call(o.ufl_operands[1])))

    def not_condition(self, o):
        return prim.LogicalNot(self.call(o.ufl_operands[0]))

    #
    # NB: Geometry and quadrature related handlers have been moved into configurable mixin classes!
    #

    #
    # Equality/Hashability of the visitor
    # In order to pass this visitor into (cached) generator functions, it is beneficial
    # to add dummy hashability to this class. A generator will *never* yield two different
    # results for two different visitor instances. Do not use this for any other purpose.
    #

    def __eq__(self, other):
        return isinstance(other, UFL2LoopyVisitor)

    def __hash__(self):
        return 0
