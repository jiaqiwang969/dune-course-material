from dune.codegen.generation import (domain,
                                     function_mangler,
                                     get_global_context_value,
                                     globalarg,
                                     iname,
                                     instruction,
                                     kernel_cached,
                                     loopy_class_member,
                                     preamble,
                                     quadrature_mixin,
                                     temporary_variable,
                                     )
from dune.codegen.sumfact.tabulation import (quadrature_points_per_direction,
                                             local_quadrature_points_per_direction,
                                             name_oned_quadrature_points,
                                             name_oned_quadrature_weights,
                                             )
from dune.codegen.pdelab.argument import name_accumulation_variable
from dune.codegen.pdelab.geometry import (local_dimension,
                                          world_dimension,
                                          )
from dune.codegen.pdelab.quadrature import GenericQuadratureMixin
from dune.codegen.options import get_form_option
from dune.codegen.loopy.target import dtype_floatingpoint

from loopy import CallMangleInfo
from loopy.symbolic import FunctionIdentifier
from loopy.types import NumpyType

from pymbolic.primitives import (Call,
                                 Product,
                                 Subscript,
                                 Variable,
                                 )

import pymbolic.primitives as prim
import loopy as lp
import numpy as np


@quadrature_mixin("sumfact")
class SumfactQuadratureMixin(GenericQuadratureMixin):
    def quadrature_inames(self):
        info = self.current_info[1]
        if info is not None:
            info = info.element

        return _quadrature_inames(info)

    def quadrature_weight(self, o):
        # Quadrature points per (local) direction
        dim = local_dimension()
        local_qps_per_dir = local_quadrature_points_per_direction()
        local_qps_per_dir_str = '_'.join(map(str, local_qps_per_dir))
        name = "quad_weights_dim{}_num{}".format(dim, local_qps_per_dir_str)

        # Add a class member
        loopy_class_member(name,
                           shape=local_qps_per_dir,
                           classtag="operator",
                           dim_tags=",".join(["f"] * dim),
                           managed=True,
                           potentially_vectorized=True,
                           )

        # Precompute it in the constructor
        inames = constructor_quadrature_inames(dim)
        assignee = prim.Subscript(prim.Variable(name), tuple(prim.Variable(i) for i in inames))
        expression = prim.Product(tuple(Subscript(Variable(name_oned_quadrature_weights(local_qps_per_dir[index])),
                                                  (prim.Variable(iname),)) for index, iname in enumerate(inames)))
        instruction(assignee=assignee,
                    expression=expression,
                    within_inames=frozenset(inames),
                    kernel="operator",
                    )

        self.quadrature_inames()
        ret = prim.Subscript(lp.symbolic.TaggedVariable(name, "operator_precomputed"),
                             tuple(prim.Variable(i) for i in self.quadrature_inames()))

        # Multiply the accumulation weight
        baseweight = 1.0
        if get_form_option("fastdg"):
            baseweight = prim.Call(BaseWeight(name_accumulation_variable()), ())

        return prim.Product((baseweight, ret))

    def quadrature_position(self, index=None):
        assert index is not None
        dim = local_dimension()
        qps_per_dir = quadrature_points_per_direction()
        local_qps_per_dir = local_quadrature_points_per_direction()
        local_qps_per_dir_str = '_'.join(map(str, local_qps_per_dir))
        name = "quad_points_dim{}_num{}_localdir{}".format(dim, local_qps_per_dir_str, index)

        loopy_class_member(name,
                           shape=local_qps_per_dir,
                           classtag="operator",
                           dim_tags=",".join(["f"] * dim),
                           managed=True,
                           potentially_vectorized=True,
                           )

        # Precompute it in the constructor
        inames = constructor_quadrature_inames(dim)
        assignee = prim.Subscript(prim.Variable(name), tuple(prim.Variable(i) for i in inames))
        expression = Subscript(Variable(name_oned_quadrature_points(local_qps_per_dir[index])),
                               (prim.Variable(inames[index])))
        instruction(assignee=assignee,
                    expression=expression,
                    within_inames=frozenset(inames),
                    kernel="operator",
                    )

        return prim.Subscript(lp.symbolic.TaggedVariable(name, "operator_precomputed"),
                              tuple(prim.Variable(i) for i in self.quadrature_inames())
                              )


class BaseWeight(FunctionIdentifier):
    def __init__(self, accumobj):
        self.accumobj = accumobj

    def __getinitargs__(self):
        return (self.accumobj,)

    @property
    def name(self):
        return '{}.weight'.format(self.accumobj)

    def operations(self):
        return 0


@function_mangler
def base_weight_function_mangler(target, func, dtypes):
    if isinstance(func, BaseWeight):
        return CallMangleInfo(func.name, (NumpyType(dtype_floatingpoint()),), ())


@kernel_cached
def _quadrature_inames(element):
    if element is None:
        names = tuple("quad_{}".format(d) for d in range(local_dimension()))
    else:
        from ufl import FiniteElement, TensorProductElement
        assert isinstance(element, (FiniteElement, TensorProductElement))
        from dune.codegen.pdelab.driver import FEM_name_mangling
        names = tuple("quad_{}_{}".format(FEM_name_mangling(element), d) for d in range(local_dimension()))

    local_qps_per_dir = local_quadrature_points_per_direction()
    domain(names, local_qps_per_dir)
    return names


@iname(kernel="operator")
def constructor_quad_iname(name, d, bound):
    name = "{}_localdim{}".format(name, d)
    domain(name, bound, kernel="operator")
    return name


def constructor_quadrature_inames(dim):
    local_qps_per_dir = local_quadrature_points_per_direction()
    local_qps_per_dir_str = '_'.join(map(str, local_qps_per_dir))
    name = "quadiname_dim{}_num{}".format(dim, local_qps_per_dir_str)
    return tuple(constructor_quad_iname(name, d, local_qps_per_dir[d]) for d in range(local_dimension()))


def additional_inames(visitor):
    """Return inames for iterating over ansatz space in the case of jacobians
    """
    info = visitor.current_info[1]
    if info is None:
        element = None
    else:
        element = info.element

    if element is not None:
        from dune.codegen.pdelab.restriction import Restriction
        restriction = Restriction.NONE
        if get_global_context_value("integral_type") == "interior_facet":
            restriction = Restriction.POSITIVE
        lfs_inames = visitor.lfs_inames(element, restriction)
        return lfs_inames
    else:
        return ()
