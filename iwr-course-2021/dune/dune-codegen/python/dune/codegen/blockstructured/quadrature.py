import math

from dune.codegen.error import CodegenError
from dune.codegen.generation import quadrature_mixin, iname, domain, kernel_cached, globalarg, transform
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.geometry import local_dimension
from dune.codegen.pdelab.quadrature import GenericQuadratureMixin, quadrature_order
from dune.codegen.blockstructured.tools import name_point_in_macro, sub_element_inames, remove_sub_element_inames
import pymbolic.primitives as prim


@quadrature_mixin("blockstructured")
class BlockstructuredQuadratureMixin(GenericQuadratureMixin):
    @staticmethod
    def _subscript_without_sub_element_inames(s):
        return prim.Subscript(s.aggregate, remove_sub_element_inames(s.index_tuple))

    @kernel_cached
    def _prioritize_loops(self, inames):
        from loopy.transform.iname import prioritize_loops
        transform(prioritize_loops, inames)

    def quadrature_position_in_micro(self, index=None):
        from dune.codegen.pdelab.geometry import local_dimension
        dim = local_dimension()
        order = quadrature_order()
        name = "qp_dim{}_order{}".format(dim, order)

        shape = (estimate_quadrature_bound(), dim)
        globalarg(name, shape=shape, managed=False)
        self.define_quadrature_points(name)

        qp = prim.Subscript(prim.Variable(name), tuple(prim.Variable(i) for i in self.quadrature_inames_in_micro()))

        if index is not None:
            qp = prim.Subscript(qp, (index,))

        return qp

    def quadrature_position_in_macro(self, index=None):
        original = self.quadrature_position_in_micro(index)
        qp = prim.Variable(name_point_in_macro(original, self), )
        if index is not None:
            return prim.Subscript(qp, (index,))
        else:
            return qp

    def quadrature_position(self, index=None):
        raise CodegenError('Decide if the quadrature point is in the macro or micro element')

    def quadrature_inames(self):
        inames = (quadrature_iname(),) + sub_element_inames()
        if get_form_option("blockstructured_prioritize_quad_loop"):
            self._prioritize_loops(reversed(inames))
        else:
            self._prioritize_loops(inames)
        return inames

    def quadrature_inames_in_micro(self):
        return (quadrature_iname(),)

    def quadrature_weight(self, o):
        return self._subscript_without_sub_element_inames(super().quadrature_weight(o))


def estimate_quadrature_bound():
    order = quadrature_order()
    n_points = math.ceil((order + 1) / 2) ** local_dimension()
    return n_points


@iname
def quadrature_iname():
    domain("q", estimate_quadrature_bound())
    return "q"
