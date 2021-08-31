from dune.codegen.generation import kernel_cached, valuearg
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.argument import CoefficientAccess
from dune.codegen.blockstructured.tools import micro_index_to_macro_index, sub_element_inames, name_container_alias
from loopy.types import NumpyType
import pymbolic.primitives as prim


# TODO remove the need for element
@kernel_cached
def pymbolic_coefficient(container, lfs, element, index):
    # TODO introduce a proper type for local function spaces!
    if isinstance(lfs, str):
        valuearg(lfs, dtype=NumpyType("str"))

    # If the LFS is not yet a pymbolic expression, make it one
    if not isinstance(lfs, prim.Expression):
        lfs = prim.Variable(lfs)

    # use higher order FEM index instead of Q1 index
    subelem_inames = sub_element_inames()
    coeff_alias = name_container_alias(container, lfs, element)
    return prim.Subscript(prim.Variable(coeff_alias), tuple(prim.Variable(i) for i in subelem_inames + index))
