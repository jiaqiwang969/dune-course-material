""" Function manglers for math functions in C++ """

from dune.codegen.generation import (function_mangler,
                                     include_file,
                                     post_include
                                     )

from loopy import CallMangleInfo
from loopy.types import to_loopy_type


def using_std_statement(name):
    post_include("using std::{};".format(name), filetag="operatorfile")


@function_mangler
def dune_math_manglers(kernel, name, arg_dtypes):
    if name == "exp":
        dt = arg_dtypes[0]
        using_std_statement(name)
        include_file("dune/codegen/common/vectorclass.hh", filetag="operatorfile")
        return CallMangleInfo("exp",
                              arg_dtypes,
                              arg_dtypes,
                              )

    if name == "sqrt":
        dt = arg_dtypes[0]
        using_std_statement(name)
        return CallMangleInfo("sqrt",
                              arg_dtypes,
                              arg_dtypes,
                              )

    if name == "max":
        dt = max(arg_dtypes, key=lambda dt: dt.itemsize)
        using_std_statement(name)
        return CallMangleInfo("max",
                              (dt,),
                              (dt,) * len(arg_dtypes),
                              )

    if name == "min":
        dt = max(arg_dtypes, key=lambda dt: dt.itemsize)
        using_std_statement(name)
        return CallMangleInfo("min",
                              (dt,),
                              (dt,) * len(arg_dtypes),
                              )

    if name == 'abs':
        dt = arg_dtypes[0]
        using_std_statement(name)
        return CallMangleInfo("abs", arg_dtypes, arg_dtypes)


@function_mangler
def get_time_function_mangler(kernel, name, arg_dtypes):
    """ The getTime method is defined on local operators once they inherit from
    InstationaryLocalOperatorDefaultMethods
    """
    if name == "getTime":
        assert(len(arg_dtypes) == 0)
        from dune.codegen.loopy.target import dtype_floatingpoint
        return CallMangleInfo("this->getTime", (to_loopy_type(dtype_floatingpoint()),), ())
