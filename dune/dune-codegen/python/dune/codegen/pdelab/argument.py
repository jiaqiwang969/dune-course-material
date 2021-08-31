""" Generator functions related to any input and output of accumulation kernels

Namely:
* Coefficient containers
* accumulation object (r, jac...)
"""

from dune.codegen.generation import (domain,
                                     function_mangler,
                                     iname,
                                     valuearg,
                                     get_global_context_value,
                                     kernel_cached,
                                     )
from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.pdelab.index import name_index
from dune.codegen.pdelab.spaces import lfs_iname
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.ufl.modified_terminals import Restriction
from dune.codegen.options import get_form_option

from pymbolic.primitives import Call, Subscript, Variable

from loopy import CallMangleInfo
from loopy.symbolic import FunctionIdentifier
from loopy.types import NumpyType

import numpy


class CoefficientAccess(FunctionIdentifier):
    def __init__(self, container):
        self.container = container

    def __getinitargs__(self):
        return (self.container,)

    @property
    def name(self):
        return self.container


@function_mangler
def coefficient_mangler(target, func, dtypes):
    if isinstance(func, CoefficientAccess):
        return CallMangleInfo(func.name, (NumpyType(dtype_floatingpoint()),), (NumpyType(str), NumpyType(numpy.int32)))


class PDELabAccumulationFunction(FunctionIdentifier):
    def __init__(self, accumobj, rank):
        self.accumobj = accumobj
        self.rank = rank

        assert rank in (1, 2)

    def __getinitargs__(self):
        return (self.accumobj, self.rank)

    @property
    def name(self):
        return '{}.accumulate'.format(self.accumobj)


@function_mangler
def accumulation_mangler(target, func, dtypes):
    if isinstance(func, PDELabAccumulationFunction):
        if func.rank == 1:
            return CallMangleInfo(func.name,
                                  (),
                                  (NumpyType(str),
                                   NumpyType(numpy.int32),
                                   NumpyType(dtype_floatingpoint()),
                                   )
                                  )
        if func.rank == 2:
            return CallMangleInfo(func.name,
                                  (),
                                  (NumpyType(str),
                                   NumpyType(numpy.int32),
                                   NumpyType(str),
                                   NumpyType(numpy.int32),
                                   NumpyType(dtype_floatingpoint()),
                                   )
                                  )


def name_coefficientcontainer(restriction):
    name = restricted_name("x", restriction)
    return name


def name_applycontainer(restriction):
    name = restricted_name("z", restriction)
    return name


@kernel_cached
def pymbolic_coefficient(container, lfs, index):
    # TODO introduce a proper type for local function spaces!
    if isinstance(lfs, str):
        valuearg(lfs, dtype=NumpyType("str"))

    # If the LFS is not yet a pymbolic expression, make it one
    from pymbolic.primitives import Expression
    if not isinstance(lfs, Expression):
        lfs = Variable(lfs)

    if isinstance(index, str):
        index = Variable(index)

    return Call(CoefficientAccess(container), (lfs, index,))


def type_coefficientcontainer():
    return "X"


def type_linearizationpointcontainer():
    return "Z"


def name_jacobian(restriction1, restriction2):
    # Restrictions may only differ if NONE
    if (restriction1 == Restriction.NONE) or (restriction2 == Restriction.NONE):
        assert restriction1 == restriction2
    return restricted_name(restricted_name("jac", restriction1), restriction2)


def type_jacobian():
    return "J"


def name_residual(restriction):
    return restricted_name("r", restriction)


def type_residual():
    return "R"


def name_accumulation_variable(restrictions=None):
    ft = get_global_context_value("form_type")
    measure = get_global_context_value("integral_type")
    if ft == 'residual' or ft == 'jacobian_apply':
        if restrictions is None:
            if measure == "cell":
                restrictions = (Restriction.NONE,)
            else:
                restrictions = (Restriction.POSITIVE,)
        if get_form_option("block_preconditioner_pointdiagonal"):
            restrictions = restrictions[:1]
        return name_residual(*restrictions)
    if ft == 'jacobian':
        if restrictions is None:
            if measure == "cell":
                restrictions = (Restriction.NONE, Restriction.NONE)
            else:
                restrictions = (Restriction.POSITIVE, Restriction.POSITIVE)
        return name_jacobian(*restrictions)
    assert False


def type_accumulation_variable():
    ft = get_global_context_value("form_type")
    if ft == 'residual' or ft == 'jacobian_apply':
        return type_residual()
    if ft == 'jacobian':
        return type_jacobian()
    assert False
