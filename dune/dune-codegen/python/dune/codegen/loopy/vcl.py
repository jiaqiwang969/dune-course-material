"""
Our extensions to the loopy type system
"""
from dune.codegen.options import get_option
from dune.codegen.generation import function_mangler, include_file

import loopy as lp
import numpy as np


class VCLTypeRegistry:
    pass


def _populate_vcl_type_registry():
    VCLTypeRegistry.types = {}
    VCLTypeRegistry.names = {}

    # The base types that we are working with!
    for base_name, base_type, abbrev in [('float', np.float32, 'f'),
                                         ('double', np.float64, 'd'),
                                         ]:
        # The vector width in bits we are considering!
        for vector_bits in [128, 256, 512]:
            # Calculate the vector lane width
            count = vector_bits // (np.dtype(base_type).itemsize * 8)

            # Define the name of this vector type
            name = "Vec{}{}".format(count, abbrev)

            # Construct the numpy dtype!
            fieldnames = tuple(chr(ord("x") + i) for i in range(count))
            dtype = np.dtype(dict(names=fieldnames,
                                  formats=[base_type] * count,
                                  )
                             )

            VCLTypeRegistry.types[np.dtype(base_type), count] = dtype
            VCLTypeRegistry.names[dtype] = name


_populate_vcl_type_registry()


def get_vcl_type_size(nptype, register_size=None):
    if register_size is None:
        register_size = get_option("max_vector_width")

    return register_size // (np.dtype(nptype).itemsize * 8)


def get_vcl_type(nptype, register_size=None, vector_width=None):
    if vector_width is None:
        vector_width = get_vcl_type_size(nptype, register_size)

    return VCLTypeRegistry.types[np.dtype(nptype), vector_width]


def get_vcl_typename(nptype, register_size=None, vector_width=None):
    vcltype = get_vcl_type(nptype, register_size=register_size, vector_width=vector_width)
    return VCLTypeRegistry.names[vcltype]


class ExplicitVCLCast(lp.symbolic.FunctionIdentifier):
    def __init__(self, nptype, vector_width=None):
        self.nptype = nptype
        if vector_width is None:
            vector_width = get_vcl_type_size(nptype)
        self.vector_width = vector_width

    def __getinitargs__(self):
        return (self.nptype, self.vector_width)

    @property
    def name(self):
        return get_vcl_typename(self.nptype, vector_width=self.vector_width)


class VCLLowerUpperLoad(ExplicitVCLCast):
    pass


@function_mangler
def vcl_cast_mangler(knl, func, arg_dtypes):
    if isinstance(func, VCLLowerUpperLoad):
        return lp.CallMangleInfo(func.name,
                                 (lp.types.NumpyType(func.nptype),),
                                 arg_dtypes)

    if isinstance(func, ExplicitVCLCast):
        return lp.CallMangleInfo(func.name, (lp.types.NumpyType(func.nptype),), (arg_dtypes[0],))


class VCLPermute(lp.symbolic.FunctionIdentifier):
    def __init__(self, nptype, vector_width, permutation):
        self.nptype = nptype
        self.vector_width = vector_width
        self.permutation = permutation

    def __getinitargs__(self):
        return (self.nptype, self.vector_width, self.permutation)

    @property
    def name(self):
        return "permute{}<{}>".format(get_vcl_typename(self.nptype, vector_width=self.vector_width)[-2],
                                      ','.join(map(str, self.permutation)))


@function_mangler
def vcl_function_mangler(knl, func, arg_dtypes):
    if func == "mul_add":
        dtype = arg_dtypes[0]
        vcl = lp.types.NumpyType(get_vcl_type(dtype))
        return lp.CallMangleInfo("mul_add", (vcl,), (vcl, vcl, vcl))

    if func == "select":
        dtype = arg_dtypes[0]
        vcl = lp.types.NumpyType(get_vcl_type(dtype))
        return lp.CallMangleInfo("select", (vcl,), (vcl, vcl, vcl))

    if func in ("horizontal_add", "horizontal_add_lower", "horizontal_add_upper"):
        if get_option("permuting_horizontal_add"):
            func = "permuting_{}".format(func)

        dtype = arg_dtypes[0]
        vcl = lp.types.NumpyType(get_vcl_type(dtype))

        if get_option("opcounter"):
            include_file("dune/codegen/sumfact/oc_horizontaladd.hh", filetag="operatorfile")
        else:
            include_file("dune/codegen/sumfact/horizontaladd.hh", filetag="operatorfile")

        return lp.CallMangleInfo(func, (lp.types.NumpyType(dtype.dtype),), (vcl,))

    if isinstance(func, VCLPermute):
        dtype = arg_dtypes[0]
        vcl = lp.types.NumpyType(get_vcl_type(dtype))
        return lp.CallMangleInfo(func.name, (vcl,), (vcl,))


class VCLLoad(lp.symbolic.FunctionIdentifier):
    def __init__(self, vec):
        self.vec = vec

    def __getinitargs__(self):
        return (self.vec,)

    @property
    def name(self):
        return "{}.load".format(self.vec)


class VCLStore(lp.symbolic.FunctionIdentifier):
    def __init__(self, vec):
        self.vec = vec

    def __getinitargs__(self):
        return (self.vec,)

    @property
    def name(self):
        return "{}.store".format(self.vec)


@function_mangler
def vcl_store_and_load_mangler(knl, func, arg_dtypes):
    if isinstance(func, VCLLoad):
        return lp.CallMangleInfo(func.name, (), (lp.types.NumpyType(np.int32),))

    if isinstance(func, VCLStore):
        return lp.CallMangleInfo(func.name, (), (lp.types.NumpyType(np.int32),))
