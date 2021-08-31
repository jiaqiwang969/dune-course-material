from dune.codegen.ufl.modified_terminals import Restriction

from dune.codegen.pdelab.argument import name_coefficientcontainer
from dune.codegen.pdelab.geometry import world_dimension, local_dimension
from dune.codegen.generation import (class_member,
                                     domain,
                                     function_mangler,
                                     generator_factory,
                                     get_global_context_value,
                                     iname,
                                     include_file,
                                     initializer_list,
                                     instruction,
                                     loopy_class_member,
                                     preamble,
                                     silenced_warning,
                                     temporary_variable,
                                     transform,
                                     valuearg
                                     )
from dune.codegen.loopy.target import dtype_floatingpoint, type_floatingpoint
from dune.codegen.loopy.vcl import ExplicitVCLCast, get_vcl_type_size
from dune.codegen.options import get_option
from dune.codegen.pdelab.localoperator import name_domain_field
from dune.codegen.pdelab.quadrature import quadrature_order
from dune.codegen.tools import maybe_wrap_subscript, ceildiv
from loopy import CallMangleInfo
from loopy.symbolic import FunctionIdentifier
from loopy.types import NumpyType

from pytools import ImmutableRecord, product

import pymbolic.primitives as prim
import loopy as lp
import numpy as np


class BasisTabulationMatrixBase(object):
    pass


class BasisTabulationMatrix(BasisTabulationMatrixBase, ImmutableRecord):
    def __init__(self,
                 basis_size=None,
                 transpose=False,
                 derivative=False,
                 face=None,
                 direction=None,
                 slice_size=None,
                 slice_index=None,
                 additional_tabulation=None,
                 ):
        """
        Arguments:
        ----------
        basis_size: Number of 1D basis functions in this direction
        transpose: Do we need the transposed of this matrix
        derivative: Do we use derivaties of the basis functions for this direction
        face: On a face with the normal direction equal to direction this is facemod (else it is None)
        direction: Direction corresponding to this matrix
        slice_size: Number of slices for this direction
        slice_index: To which slice does this belong
        additional_tabulation: A factor to be multiplied with this basis tabulation matrix.
        """
        assert(isinstance(basis_size, int))
        ImmutableRecord.__init__(self,
                                 basis_size=basis_size,
                                 transpose=transpose,
                                 derivative=derivative,
                                 face=face,
                                 direction=direction,
                                 slice_size=slice_size,
                                 slice_index=slice_index,
                                 additional_tabulation=additional_tabulation,
                                 )

    @property
    def _shortname(self):
        infos = ["d{}".format(self.basis_size),
                 "q{}".format(self.quadrature_size)]

        if self.transpose:
            infos.append("T")

        if self.derivative:
            infos.append("dx")

        if self.face is not None:
            infos.append("f{}".format(self.face))

        if self.slice_size is not None:
            infos.append("s{}".format(self.slice_index))

        if self.additional_tabulation is not None:
            infos.append("prod{}".format(self.additional_tabulation._shortname))

        return "".join(infos)

    def __str__(self):
        return "Theta_{}".format(self._shortname)

    @property
    def rows(self):
        if self.transpose:
            return self.basis_size
        else:
            return self.quadrature_size

    @property
    def cols(self):
        if self.transpose:
            return self.quadrature_size
        else:
            return self.basis_size

    @property
    def quadrature_size(self):
        size = quadrature_points_per_direction()
        size = size[self.direction]
        if self.face is not None:
            size = 1
        if self.slice_size is not None:
            size = ceildiv(size, self.slice_size)
        return size

    def pymbolic(self, indices):
        name = str(self)
        define_theta(name, self)
        ret = prim.Subscript(prim.Variable(name), indices)

        return ret

    @property
    def vectorized(self):
        return False

    #
    # Implement properties needed by cost models
    #

    @property
    def memory_traffic(self):
        """ The total number of bytes needed from RAM for the kernel
        to be executed - neglecting the existence of caches of course
        """
        return mat.rows * mat.cols


class BasisTabulationMatrixArray(BasisTabulationMatrixBase):
    def __init__(self, tabs, width=None):
        assert isinstance(tabs, tuple)

        # Assert that all the basis tabulations match in size!
        assert len(set(t.basis_size for t in tabs)) == 1
        assert len(set(t.transpose for t in tabs)) == 1
        self.tabs = tabs

        if width is None:
            width = len(tabs)
        self.width = width

    def __str__(self):
        return "Theta{}".format("_".join((t._shortname for t in self.tabs)))

    @property
    def quadrature_size(self):
        return self.tabs[0].quadrature_size

    @property
    def basis_size(self):
        return self.tabs[0].basis_size

    @property
    def transpose(self):
        return self.tabs[0].transpose

    @property
    def face(self):
        return self.tabs[0].face

    @property
    def derivative(self):
        return tuple(t.derivative for t in self.tabs)

    @property
    def slice_size(self):
        return self.tabs[0].slice_size

    @property
    def slice_index(self):
        return tuple(t.slice_index for t in self.tabs)

    @property
    def rows(self):
        if self.transpose:
            return self.basis_size
        else:
            return self.quadrature_size

    @property
    def cols(self):
        if self.transpose:
            return self.quadrature_size
        else:
            return self.basis_size

    def pymbolic(self, indices):
        assert len(indices) == 3

        # Check whether we can realize this by broadcasting the values of a simple tabulation
        if len(set(self.tabs)) == 1:
            theta = self.tabs[0].pymbolic(indices[:-1])
            return prim.Call(ExplicitVCLCast(dtype_floatingpoint(), vector_width=get_vcl_type_size(dtype_floatingpoint())), (theta,))

        name = str(self)

        for i, tab in enumerate(self.tabs):
            define_theta(name, tab, additional_indices=(i,), width=self.width)

        # Apply padding to those fields not used. This is necessary because you may get memory
        # initialized with NaN and those NaNs will screw the horizontal_add.
        i, j = theta_inames(self.rows, self.cols)
        for index in set(range(self.width)) - set(range(len(self.derivative))):
            instruction(assignee=prim.Subscript(prim.Variable(name), (prim.Variable(i), prim.Variable(j), index)),
                        expression=0,
                        kernel="operator")

        member = loopy_class_member(name,
                                    classtag="operator",
                                    dim_tags="f,f,vec",
                                    shape=(self.rows, self.cols, self.width),
                                    potentially_vectorized=True,
                                    managed=True,
                                    )

        return prim.Subscript(prim.Variable(member), indices)

    @property
    def vectorized(self):
        return True

    #
    # Implement properties needed by cost models
    #

    @property
    def memory_traffic(self):
        """ The total number of bytes needed from RAM for the kernel
        to be executed - neglecting the existence of caches of course
        """
        if len(set(self.tabs)) == 1:
            factor = 1
        else:
            factor = self.width
        return factor * mat.rows * mat.cols


_quad = None


def set_quadrature_points(quad):
    assert quad is None or isinstance(quad, tuple)
    global _quad
    _quad = quad


def quadrature_points_per_direction():
    global _quad
    if _quad is not None:
        return _quad

    # Quadrature order per direction
    q = quadrature_order()
    if isinstance(q, int):
        q = (q,) * world_dimension()

    # Quadrature points in per direction
    nb_qp = tuple(order // 2 + 1 for order in q)
    _quad = nb_qp

    return nb_qp


def local_quadrature_points_per_direction():
    """On a volume this simply gives the number of quadrature points per
    direction. On a face it only returns the worlddim - 1 number of
    quadrature points belonging to this face. (Delete normal direction).
    """
    qps_per_dir = quadrature_points_per_direction()
    if local_dimension() != world_dimension():
        facedir = get_global_context_value('facedir_s')
        if not get_option("grid_unstructured"):
            assert(get_global_context_value('facedir_s') == get_global_context_value('facedir_n') or
                   get_global_context_value('integral_type') == 'exterior_facet')
        if get_option("grid_unstructured"):
            # For unstructured grids the amount of quadrature points could be different for
            # self and neighbor. For now assert that this case is not happining.
            assert len(set(qps_per_dir)) == 1
        qps_per_dir = qps_per_dir[:facedir] + qps_per_dir[facedir + 1:]
    return qps_per_dir


def polynomial_degree():
    data = get_global_context_value("data")
    form = data.object_by_name[get_form_option("form")]
    from dune.codegen.ufl.preprocess import preprocess_form
    form = preprocess_form(form).preprocessed_form
    degree = form.coefficients()[0].ufl_element().degree()
    if isinstance(degree, int):
        degree = (degree,) * world_dimension()
    return degree


def basis_functions_per_direction():
    return tuple(degree + 1 for degree in polynomial_degree())


def define_oned_quadrature_weights(name, bound):
    loopy_class_member(name,
                       classtag="operator",
                       shape=(bound,),
                       )


def name_oned_quadrature_weights(bound):
    name = "qw_num{}".format(bound)
    define_oned_quadrature_weights(name, bound)
    return name


def define_oned_quadrature_points(name, bound):
    loopy_class_member(name,
                       classtag="operator",
                       shape=(bound,),
                       )


def name_oned_quadrature_points(bound):
    name = "qp_num{}".format(bound)
    define_oned_quadrature_points(name, bound)
    return name


@class_member(classtag="operator")
def typedef_polynomials(name, degree):
    range_field = type_floatingpoint()
    domain_field = name_domain_field()

    include_file("dune/pdelab/finiteelementmap/qkdg.hh", filetag="operatorfile")

    # TODO: make switching polynomials possible
    # return "using {} = Dune::QkStuff::GaussLobattoLagrangePolynomials<{}, {}, {}>;".format(name,
    #                                                                                        domain_field,
    #                                                                                        range_field,
    #                                                                                        degree)
    return "using {} = Dune::QkStuff::EquidistantLagrangePolynomials<{}, {}, {}>;".format(name,
                                                                                          domain_field,
                                                                                          range_field,
                                                                                          degree)


def type_polynomials(degree):
    name = "Polynomials1D_Degree{}".format(degree)
    typedef_polynomials(name, degree)
    return name


@class_member(classtag="operator")
def define_polynomials(name, degree):
    polynomials_type = type_polynomials(degree)
    return "{} {};".format(polynomials_type, name)


def name_polynomials(degree):
    name = "poly_degree{}".format(degree)
    define_polynomials(name, degree)
    return name


def sort_quadrature_points_weights(qp, qw, bound):
    range_field = type_floatingpoint()
    domain_field = name_domain_field()
    include_file("dune/codegen/sumfact/onedquadrature.hh", filetag="operatorfile")
    return frozenset({instruction(code="onedQuadraturePointsWeights<{}, {}, {}>({}, {});"
                                  .format(range_field, domain_field, bound, qp, qw),
                                  assignees=frozenset({qp, qw}),
                                  read_variables=frozenset({qp, qw}),
                                  kernel="operator",
                                  ),
                      })


@iname(kernel="operator")
def _theta_iname(name, bound):
    domain(name, bound, kernel="operator")
    return name


def theta_inames(rows, cols):
    rowname = "Theta_{}x{}_row".format(rows, cols)
    colname = "Theta_{}x{}_col".format(rows, cols)
    return _theta_iname(rowname, rows), _theta_iname(colname, cols)


class PolynomialLookup(FunctionIdentifier):
    def __init__(self, pol, derivative):
        self.pol = pol
        self.derivative = derivative

    def __getinitargs__(self):
        return (self.pol, self.derivative)

    @property
    def name(self):
        return "{}.{}".format(self.pol, "dp" if self.derivative else "p")


@function_mangler
def polynomial_lookup_mangler(target, func, dtypes):
    if isinstance(func, PolynomialLookup):
        dtype = dtype_floatingpoint()
        return CallMangleInfo(func.name, (NumpyType(dtype),), (NumpyType(np.int32), NumpyType(dtype)))


def define_theta(name, tabmat, additional_indices=(), width=None):
    assert isinstance(tabmat, BasisTabulationMatrix)
    bound = tabmat.quadrature_size
    if tabmat.slice_size is not None:
        bound *= tabmat.slice_size

    degree = tabmat.basis_size - 1
    polynomials = name_polynomials(degree)

    shape = (tabmat.rows, tabmat.cols)
    dim_tags = "f,f"
    if additional_indices:
        dim_tags = dim_tags + ",c"
        shape = shape + (width,)

    loopy_class_member(name,
                       shape=shape,
                       classtag="operator",
                       dim_tags=dim_tags,
                       managed=True,
                       potentially_vectorized=True,
                       )

    i, j = theta_inames(tabmat.rows, tabmat.cols)
    i = prim.Variable(i)
    j = prim.Variable(j)

    inames = [i, j]
    if tabmat.transpose:
        inames = [j, i]

    if tabmat.slice_size is not None:
        inames[0] = tabmat.slice_size * inames[0] + tabmat.slice_index

    args = [inames[1]]

    dep = frozenset()
    if tabmat.face is None:
        qp = name_oned_quadrature_points(bound)
        qw = name_oned_quadrature_weights(bound)
        dep = sort_quadrature_points_weights(qp, qw, bound)
        args.append(prim.Subscript(prim.Variable(qp), (inames[0],)))
    else:
        args.append(tabmat.face)

    # Get right hand side of basis evaluation matrix assignment
    expr = prim.Call(PolynomialLookup(polynomials, tabmat.derivative), tuple(args))

    # Maybe multiply another matrix (needed for the very special case of assembling point diagonals)
    if tabmat.additional_tabulation is not None:
        expr = prim.Product((expr, prim.Call(PolynomialLookup(polynomials, tabmat.additional_tabulation.derivative), tuple(args))))

    instruction(assignee=prim.Subscript(prim.Variable(name), (i, j) + additional_indices),
                expression=expr,
                kernel="operator",
                depends_on=dep,
                )


def construct_basis_matrix_sequence(transpose=False, derivative=None, facedir=None, facemod=None, basis_size=None, additional_sequence=None):
    dim = world_dimension()
    result = [None] * dim
    if additional_sequence is None:
        additional_sequence = [None] * dim
    quadrature_size = quadrature_points_per_direction()
    assert (basis_size is not None)
    if facedir is not None:
        quadrature_size = quadrature_size[:facedir] + (1,) + quadrature_size[facedir:]

    for i, add_seq in zip(range(dim), additional_sequence):
        onface = None
        if facedir == i:
            onface = facemod

        result[i] = BasisTabulationMatrix(direction=i,
                                          basis_size=basis_size[i],
                                          transpose=transpose,
                                          derivative=derivative == i,
                                          face=onface,
                                          additional_tabulation=add_seq)

    return tuple(result)
