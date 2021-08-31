""" This module is loaded instead of ufl when executing .ufl files.
So, this module contains all our extensions and monkey patches to
UFL.
"""
from dune.codegen.error import CodegenUFLError

import ufl

from ufl import *


class TrialFunction(ufl.Coefficient):
    """ A coefficient that always takes the reserved index 0 """
    def __init__(self, element, count=None):
        if count is not None and count != 0:
            raise CodegenUFLError("The trial function must be the coefficient of index 0 in uflpdelab")
        ufl.Coefficient.__init__(self, element, count=0)


class Coefficient(ufl.Coefficient):
    """ A coefficient that honors the reserved index 0. """
    def __init__(self, element, count=None, cargo={}):
        """The cargo member can be used to transport data through the Coefficient
        without UFL knowing about it. Use case: Transport is_dirichlet data
        through the coefficient for operator splitting
        """
        self.cargo = cargo
        if count == 0:
            raise CodegenUFLError("The coefficient of index 0 is reserved for the trial function in uflpdelab")
        if count == 1:
            raise CodegenUFLError("The coefficient of index 1 is reserved for the jacobian apply vector in uflpdelab")
        if count == 2:
            raise CodegenUFLError("The coefficient of index 2 is reserved for the time variable in uflpdelab")
        if count is None and ufl.Coefficient._globalcount < 3:
            count = 3
        ufl.Coefficient.__init__(self, element, count)

    def codegen_cargo(self, key):
        # Transport data through the Coefficient
        return self.cargo.get(key, None)


def split(obj):
    return ufl.split_functions.split(obj)


def Coefficients(element, cargo=None):
    return split(Coefficient(element, cargo=cargo))


def TestFunctions(element):
    return split(TestFunction(element))


def TrialFunctions(element):
    return split(TrialFunction(element))


def get_time(cell):
    return Constant(cell, count=2)
