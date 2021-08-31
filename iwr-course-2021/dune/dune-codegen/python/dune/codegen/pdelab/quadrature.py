import numpy

from dune.codegen.generation import (class_member,
                                     domain,
                                     get_global_context_value,
                                     globalarg,
                                     iname,
                                     include_file,
                                     instruction,
                                     kernel_cached,
                                     preamble,
                                     quadrature_mixin,
                                     temporary_variable,
                                     valuearg,
                                     )
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.pdelab.localoperator import name_ansatz_gfs_constructor_param
from dune.codegen.options import get_form_option

from pymbolic.primitives import Variable, Subscript
import pymbolic.primitives as prim


@quadrature_mixin("base")
class QuadratureMixinBase(object):
    def quad_unhandled(self, o):
        raise NotImplementedError("Quadrature Mixins should handle {}".format(type(o)))

    quadrature_weight = quad_unhandled

    def quadrature_inames(self):
        raise NotImplementedError("Quadrature mixins should provide the quadrature inames!")

    def quadrature_position(self, index=None):
        raise NotImplementedError("Quadrature mixins should provide the quadrature position")


@quadrature_mixin("generic")
class GenericQuadratureMixin(QuadratureMixinBase):
    def quadrature_weight(self, o):
        # Create a name that has all the necessary quantities mangled in
        from dune.codegen.pdelab.geometry import local_dimension
        dim = local_dimension()
        order = quadrature_order()
        name = "qw_dim{}_order{}".format(dim, order)

        shape = name_quadrature_bound()
        globalarg(name, shape=(shape,))
        self.define_quadrature_weights(name)

        return prim.Subscript(prim.Variable(name),
                              tuple(prim.Variable(i) for i in self.quadrature_inames()))

    @class_member(classtag="operator")
    def define_quadrature_weights(self, name):
        rf = type_floatingpoint()
        from dune.codegen.pdelab.geometry import local_dimension
        dim = local_dimension()
        self.eval_quadrature_weights(name)
        return "mutable std::vector<typename Dune::QuadraturePoint<{}, {}>::Field> {};".format(rf, dim, name)

    @preamble(kernel="operator")
    def eval_quadrature_weights(self, name):
        gfs = name_ansatz_gfs_constructor_param()
        quad_order = quadrature_order()
        include_file("dune/codegen/localbasiscache.hh", filetag='operatorfile')
        entity = "{}.gridView().template begin<0>()".format(gfs)
        if self.measure != "cell":
            entity = "{}.gridView().ibegin(*({}))".format(gfs, entity)
        return "fillQuadratureWeightsCache({}->geometry(), {}, {});".format(entity, quad_order, name)

    def quadrature_inames(self):
        return (quadrature_iname(),)

    @kernel_cached
    def quadrature_position(self, index=None):
        from dune.codegen.pdelab.geometry import local_dimension
        dim = local_dimension()
        order = quadrature_order()
        name = "qp_dim{}_order{}".format(dim, order)

        shape = (name_quadrature_bound(), dim)
        globalarg(name, shape=shape, managed=False)
        self.define_quadrature_points(name)

        qp = prim.Subscript(prim.Variable(name), tuple(prim.Variable(i) for i in self.quadrature_inames()))

        if index is not None:
            qp = prim.Subscript(qp, (index,))

        return qp

    @class_member(classtag="operator")
    def define_quadrature_points(self, name):
        rf = type_floatingpoint()
        from dune.codegen.pdelab.geometry import local_dimension
        dim = local_dimension()
        self.eval_quadrature_points(name)
        return "mutable std::vector<typename Dune::QuadraturePoint<{}, {}>::Vector> {};".format(rf, dim, name)

    @preamble(kernel="operator")
    def eval_quadrature_points(self, name):
        gfs = name_ansatz_gfs_constructor_param()
        quad_order = quadrature_order()
        include_file("dune/codegen/localbasiscache.hh", filetag='operatorfile')
        entity = "{}.gridView().template begin<0>()".format(gfs)
        if self.measure != "cell":
            entity = "{}.gridView().ibegin(*({}))".format(gfs, entity)
        return "fillQuadraturePointsCache({}->geometry(), {}, {});".format(entity, quad_order, name)


@preamble
def define_quadrature_rule(name):
    include_file('dune/pdelab/common/quadraturerules.hh', filetag='operatorfile')
    from dune.codegen.pdelab.geometry import name_geometry
    geo = name_geometry()
    order = name_quadrature_order()
    return "const auto {} = quadratureRule({}, {});".format(name, geo, order)


def name_quadrature_rule():
    name = "quadrature_rule"
    define_quadrature_rule(name)
    return name


@preamble
def define_quadrature_bound(name):
    quad_rule = name_quadrature_rule()
    return "auto {} = {}.size();".format(name, quad_rule)


def name_quadrature_bound():
    name = "quadrature_size"
    define_quadrature_bound(name)

    # Quadrature bound is a valuearg for loopy
    valuearg(name, dtype=numpy.int32)

    return name


@iname
def quadrature_iname():
    domain("q", name_quadrature_bound())
    return "q"


def quadrature_preamble(visitor, code, **kw):
    kw['tags'] = kw.get('tags', frozenset({})).union(frozenset({"quad"}))
    return instruction(inames=visitor.quadrature_inames(), code=code, **kw)


def name_quadrature_point():
    # Note: Used for qp_in_inside/qp_in_outside
    return "qp"


def _estimate_quadrature_order():
    """Estimate quadrature order using polynomial degree estimation from UFL"""
    # According to UFL documentation estimate_total_polynomial_degree
    # should only be called on preprocessed forms.
    data = get_global_context_value("data")
    form = data.object_by_name[get_form_option("form")]
    from dune.codegen.ufl.preprocess import preprocess_form
    form = preprocess_form(form).preprocessed_form

    # Estimate polynomial degree of integrals of current type (eg 'Cell')
    integral_type = get_global_context_value("integral_type")
    integrals = form.integrals_by_type(integral_type)

    # Degree could be a tuple (for TensorProductElements)
    degree = integrals[0].metadata()['estimated_polynomial_degree']
    if isinstance(degree, int):
        degree = (degree,)
    polynomial_degree = [0, ] * len(degree)

    for i in integrals:
        degree = i.metadata()['estimated_polynomial_degree']
        if isinstance(degree, int):
            degree = [degree, ]
        assert(len(polynomial_degree) == len(degree))
        for i in range(len(polynomial_degree)):
            polynomial_degree[i] = max(polynomial_degree[i], degree[i])

    # Return either a tuple or an int
    polynomial_degree = tuple(polynomial_degree)
    if len(polynomial_degree) == 1:
        polynomial_degree = polynomial_degree[0]

    return polynomial_degree


def quadrature_order():
    """Get quadrature order

    Notes:

    - In PDELab quadrature order m means that integration of
      polynomials of degree m is exact.

    - If you use sum factorization and TensorProductElement it is
      possible to use a different quadrature_order per direction.
    """
    if get_form_option("quadrature_order"):
        quadrature_order = tuple(map(int, str(get_form_option("quadrature_order")).split(',')))
    else:
        quadrature_order = _estimate_quadrature_order()

    # TensorProductElements can have different quadrature order for
    # every direction so quadrature_order may be a tuple. If we do not
    # use TensorProductElements we want to return an int.
    if isinstance(quadrature_order, tuple):
        if len(quadrature_order) == 1:
            quadrature_order = quadrature_order[0]
    if isinstance(quadrature_order, tuple):
        if not get_form_option('sumfact'):
            raise NotImplementedError("Different quadrature order per direction is only implemented for kernels using sum factorization.")
        from dune.codegen.pdelab.geometry import world_dimension
        assert(len(quadrature_order) == world_dimension())

    return quadrature_order


def name_quadrature_order():
    # Quadrature order from UFL estimation
    quad_order = quadrature_order()
    return str(quad_order)
