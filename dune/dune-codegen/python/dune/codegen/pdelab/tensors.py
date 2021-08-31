""" Code generation for explicitly specified tensors """

from dune.codegen.generation import (get_counted_variable,
                                     kernel_cached,
                                     instruction,
                                     temporary_variable,
                                     )
from dune.codegen.loopy.symbolic import FusedMultiplyAdd as FMA
from loopy.match import Writes

import pymbolic.primitives as prim
import numpy as np
import loopy as lp
import itertools as it


def define_determinant(name, matrix, shape, visitor):
    temporary_variable(name, managed=True)

    assert len(shape) == 2 and shape[0] == shape[1]
    dim = shape[0]

    matrix_entry = [[prim.Subscript(prim.Variable(matrix), (i, j)) for j in range(dim)] for i in range(dim)]
    if dim == 2:
        expr_determinant = FMA(matrix_entry[0][0], matrix_entry[1][1], -1 * matrix_entry[1][0] * matrix_entry[0][1])

    elif dim == 3:
        fma_A = FMA(matrix_entry[1][1], matrix_entry[2][2], -1 * matrix_entry[1][2] * matrix_entry[2][1])
        fma_B = FMA(matrix_entry[1][0], matrix_entry[2][2], -1 * matrix_entry[1][2] * matrix_entry[2][0])
        fma_C = FMA(matrix_entry[1][0], matrix_entry[2][1], -1 * matrix_entry[1][1] * matrix_entry[2][0])

        expr_determinant = FMA(matrix_entry[0][2], fma_C,
                               FMA(matrix_entry[0][0], fma_A, -1 * matrix_entry[0][1] * fma_B))
    else:
        raise NotImplementedError()
    instruction(expression=expr_determinant,
                assignee=prim.Variable(name),
                within_inames=frozenset(visitor.quadrature_inames()),
                depends_on=frozenset({Writes(matrix)})
                )


def define_determinant_inverse(name, matrix, shape, visitor):
    det = name_determinant(matrix, shape, visitor)

    temporary_variable(name, managed=True)

    instruction(expression=prim.Quotient(1, prim.Variable(det)),
                assignee=prim.Variable(name),
                within_inames=frozenset(visitor.quadrature_inames()),
                depends_on=frozenset({Writes(matrix), Writes(det)})
                )


def define_matrix_inverse(name, name_inv, shape, visitor):
    temporary_variable(name_inv, shape=shape, managed=True)

    det_inv = name_determinant_inverse(name, shape, visitor)

    assert len(shape) == 2 and shape[0] == shape[1]
    dim = shape[0]

    matrix_entry = [[prim.Subscript(prim.Variable(name), (i, j)) for j in range(dim)] for i in range(dim)]
    assignee = [[prim.Subscript(prim.Variable(name_inv), (i, j)) for j in range(dim)] for i in range(dim)]
    exprs = [[None for _ in range(dim)] for _ in range(dim)]

    if dim == 2:
        for i in range(2):
            for j in range(2):
                sign = 1. if i == j else -1.
                exprs[i][j] = prim.Product((sign, prim.Variable(det_inv), matrix_entry[1 - i][1 - j]))
    elif dim == 3:
        exprs[0][0] = prim.Variable(det_inv) * FMA(matrix_entry[1][1], matrix_entry[2][2],
                                                   -1 * matrix_entry[1][2] * matrix_entry[2][1])
        exprs[1][0] = prim.Variable(det_inv) * FMA(matrix_entry[0][1], matrix_entry[2][2],
                                                   -1 * matrix_entry[0][2] * matrix_entry[2][1]) * -1
        exprs[2][0] = prim.Variable(det_inv) * FMA(matrix_entry[0][1], matrix_entry[1][2],
                                                   -1 * matrix_entry[0][2] * matrix_entry[1][1])

        exprs[0][1] = prim.Variable(det_inv) * FMA(matrix_entry[1][0], matrix_entry[2][2],
                                                   -1 * matrix_entry[1][2] * matrix_entry[2][0]) * -1
        exprs[1][1] = prim.Variable(det_inv) * FMA(matrix_entry[0][0], matrix_entry[2][2],
                                                   -1 * matrix_entry[0][2] * matrix_entry[2][0])
        exprs[2][1] = prim.Variable(det_inv) * FMA(matrix_entry[0][0], matrix_entry[1][2],
                                                   -1 * matrix_entry[0][2] * matrix_entry[1][0]) * -1

        exprs[0][2] = prim.Variable(det_inv) * FMA(matrix_entry[1][0], matrix_entry[2][1],
                                                   -1 * matrix_entry[1][1] * matrix_entry[2][0])
        exprs[1][2] = prim.Variable(det_inv) * FMA(matrix_entry[0][0], matrix_entry[2][1],
                                                   -1 * matrix_entry[0][1] * matrix_entry[2][0]) * -1
        exprs[2][2] = prim.Variable(det_inv) * FMA(matrix_entry[0][0], matrix_entry[1][1],
                                                   -1 * matrix_entry[0][1] * matrix_entry[1][0])
    else:
        raise NotImplementedError
    for j in range(dim):
        for i in range(dim):
            instruction(expression=exprs[i][j],
                        assignee=assignee[i][j],
                        within_inames=frozenset(visitor.quadrature_inames()),
                        depends_on=frozenset({Writes(name), Writes(det_inv)}),
                        tags=frozenset({"inversion_{}".format(name)}),
                        no_sync_with=frozenset({(lp.match.Tagged("inversion_{}".format(name)), "any")}),
                        )


def name_determinant(matrix, shape, visitor):
    name = matrix + "_det"

    define_determinant(name, matrix, shape, visitor)

    return name


def name_determinant_inverse(matrix, shape, visitor):
    name = matrix + "_det_inv"

    define_determinant_inverse(name, matrix, shape, visitor)

    return name


def name_matrix_inverse(name, shape, visitor):
    name_inv = name + "_inv"

    define_matrix_inverse(name, name_inv, shape, visitor)

    return name_inv


def define_assembled_tensor(name, expr, visitor):
    temporary_variable(name,
                       shape=expr.ufl_shape,
                       shape_impl=('fm',))
    for indices in it.product(*tuple(range(i) for i in expr.ufl_shape)):
        visitor.indices = indices
        instruction(assignee=prim.Subscript(prim.Variable(name), indices),
                    expression=visitor.call(expr),
                    forced_iname_deps=frozenset(visitor.quadrature_inames()),
                    depends_on=frozenset({lp.match.Tagged("sumfact_stage1")}),
                    tags=frozenset({"quad"}),
                    )


@kernel_cached
def name_assembled_tensor(o, visitor):
    name = get_counted_variable("assembled_tensor")
    define_assembled_tensor(name, o, visitor)
    return name


@kernel_cached
def code_generation_time_inversion(expr, visitor):
    mat = np.ndarray(expr.ufl_shape)
    for indices in it.product(*tuple(range(i) for i in expr.ufl_shape)):
        visitor.indices = indices
        val = visitor.call(expr.ufl_operands[0])
        if not isinstance(val, (float, int)):
            visitor.indices = None
            return None

        mat[indices] = val

    visitor.indices = None
    return np.linalg.inv(mat)


def pymbolic_matrix_inverse(o, visitor):
    # Try to evaluate the matrix at code generation time.
    # If this works (it does e.g. for Maxwell on structured grids)
    # we can invert the matrix at code generation time!!!
    indices = visitor.indices
    visitor.indices = None

    mat = code_generation_time_inversion(o, visitor)
    if mat is not None:
        return mat[indices]

    # If code generation time inversion failed, we assemble it in C++
    # and invert it there.
    expr = o.ufl_operands[0]
    name = name_assembled_tensor(expr, visitor)

    if expr.ufl_shape[0] <= 3:
        name = name_matrix_inverse(name, expr.ufl_shape, visitor)
    else:
        instruction(code="{}.invert();".format(name),
                    within_inames=frozenset(visitor.quadrature_inames()),
                    depends_on=frozenset({lp.match.Writes(name),
                                          lp.match.Tagged("sumfact_stage1"),
                                          }),
                    tags=frozenset({name}),
                    )

    visitor.indices = indices
    return prim.Variable(name)
