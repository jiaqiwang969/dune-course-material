from dune.codegen.ufl.modified_terminals import Restriction
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.generation import (class_member,
                                     domain,
                                     geometry_mixin,
                                     get_global_context_value,
                                     globalarg,
                                     iname,
                                     include_file,
                                     kernel_cached,
                                     preamble,
                                     temporary_variable,
                                     valuearg,
                                     )
from dune.codegen.options import get_form_option
from dune.codegen.loopy.target import dtype_floatingpoint, type_floatingpoint
from dune.codegen.pdelab.quadrature import (quadrature_preamble,
                                            )
from dune.codegen.tools import get_pymbolic_basename
from ufl.algorithms import MultiFunction
from pymbolic.primitives import Variable

from loopy.match import Writes

import numpy as np
import pymbolic.primitives as prim

from pytools import memoize


@geometry_mixin("base")
class GeometryMixinBase(object):
    """
    This mixin will be in by default by the mixin magic,
    so it should only define an interface and throw exceptions.
    """
    def geo_unhandled(self, o):
        raise NotImplementedError("Geometry Mixins should handle {}".format(type(o)))

    def jacobian(self, o):
        raise NotImplementedError("How did you get Jacobian into your form? We only support JacobianInverse right now. Report!")

    spatial_coordinate = geo_unhandled
    facet_normal = geo_unhandled
    jacobian_determinant = geo_unhandled
    jacobian_inverse = geo_unhandled
    facet_jacobian_determinant = geo_unhandled
    cell_volume = geo_unhandled
    facet_area = geo_unhandled

    def to_global(self, local):
        raise NotImplementedError("Geometry Mixins should implement a to_global mapping")

    def to_cell(self, local):
        raise NotImplementedError("Geometry Mixins should implement a to_cell mapping")


@geometry_mixin("generic")
class GenericPDELabGeometryMixin(GeometryMixinBase):
    def spatial_coordinate(self, o):
        return self.to_global(self.quadrature_position())

    def to_global(self, local):
        assert isinstance(local, prim.Expression)
        name = get_pymbolic_basename(local) + "_global"

        temporary_variable(name, shape=(world_dimension(),), shape_impl=("fv",))
        geo = name_geometry()
        code = "{} = {}.global({});".format(name,
                                            geo,
                                            local,
                                            )

        quadrature_preamble(self,
                            code,
                            assignees=frozenset({name}),
                            read_variables=frozenset({get_pymbolic_basename(local)}),
                            depends_on=frozenset({Writes(get_pymbolic_basename(local))})
                            )

        return prim.Variable(name)

    def to_cell(self, local):
        assert isinstance(local, prim.Expression)

        restriction = enforce_boundary_restriction(self)
        if restriction == Restriction.NONE:
            return local

        return self._to_cell(local, restriction)

    @kernel_cached
    def _to_cell(self, local, restriction):
        basename = get_pymbolic_basename(local)
        name = "{}_in_{}side".format(basename, "in" if restriction is Restriction.POSITIVE else "out")
        temporary_variable(name, shape=(world_dimension(),), shape_impl=("fv",))
        geo = name_in_cell_geometry(restriction)
        quadrature_preamble(self,
                            "{} = {}.global({});".format(name,
                                                         geo,
                                                         str(local),
                                                         ),
                            assignees=frozenset({name}),
                            read_variables=frozenset({get_pymbolic_basename(local)}),
                            depends_on=frozenset({Writes(get_pymbolic_basename(local))}),
                            )

        return prim.Variable(name)

    def facet_jacobian_determinant(self, o):
        name = "fdetjac"
        self.define_facet_jacobian_determinant(name)
        return prim.Variable(name)

    def define_facet_jacobian_determinant(self, name):
        # NB: This can reuse the same implementation as the cell jacobian
        #     determinant, because the obtain geometry will be a face geometry
        return self.define_jacobian_determinant(name)

    def jacobian_determinant(self, o):
        name = 'detjac'
        self.define_jacobian_determinant(name)
        return prim.Variable(name)

    def define_jacobian_determinant(self, name):
        temporary_variable(name, shape=())
        geo = name_geometry()
        pos = self.quadrature_position()
        code = "{} = {}.integrationElement({});".format(name,
                                                        geo,
                                                        str(pos),
                                                        )

        return quadrature_preamble(self,
                                   code,
                                   assignees=frozenset({name}),
                                   read_variables=frozenset({get_pymbolic_basename(pos)}),
                                   depends_on=frozenset({Writes(get_pymbolic_basename(pos))}),
                                   )

    def jacobian_inverse(self, o):
        restriction = enforce_boundary_restriction(self)

        assert(len(self.indices) == 2)
        i, j = self.indices
        self.indices = None

        name = restricted_name("jit", restriction)
        self.define_jacobian_inverse_transposed(name, restriction)

        return prim.Subscript(prim.Variable(name), (j, i))

    def define_jacobian_inverse_transposed(self, name, restriction):
        dim = world_dimension()
        temporary_variable(name, shape_impl=('fm',), shape=(dim, dim))
        geo = name_cell_geometry(restriction)
        pos = self.to_cell(self.quadrature_position())

        return quadrature_preamble(self,
                                   "{} = {}.jacobianInverseTransposed({});".format(name,
                                                                                   geo,
                                                                                   str(pos),
                                                                                   ),
                                   assignees=frozenset({name}),
                                   read_variables=frozenset({get_pymbolic_basename(pos)}),
                                   depends_on=frozenset({Writes(get_pymbolic_basename(pos))}),
                                   )

    def facet_normal(self, o):
        if self.restriction == Restriction.NEGATIVE:
            raise NotImplementedError("Inner Normals not implemented!")

        name = "unit_outer_normal"
        self.define_unit_outer_normal(name)
        return prim.Variable(name)

    def define_unit_outer_normal(self, name):
        temporary_variable(name, shape=(world_dimension(),), decl_method=declare_normal)

        ig = name_intersection_geometry_wrapper()
        qp = self.quadrature_position()
        return quadrature_preamble(self,
                                   "{} = {}.unitOuterNormal({});".format(name, ig, qp),
                                   assignees=frozenset({name}),
                                   read_variables=frozenset({get_pymbolic_basename(qp)}),
                                   depends_on=frozenset({Writes(get_pymbolic_basename(qp))}),
                                   )

    def cell_volume(self, o):
        restriction = enforce_boundary_restriction(self)
        name = restricted_name("volume", restriction)
        self.define_cell_volume(name, restriction)
        return prim.Variable(name)

    @preamble
    def define_cell_volume(self, name, restriction):
        geo = name_cell_geometry(restriction)
        valuearg(name)
        return "auto {} = {}.volume();".format(name, geo)

    def facet_area(self, o):
        name = "area"
        self.define_facet_area(name)
        return prim.Variable(name)

    @preamble
    def define_facet_area(self, name):
        geo = name_intersection_geometry()
        valuearg(name)
        return "auto {} = {}.volume();".format(name, geo)


@geometry_mixin("axiparallel")
class AxiparallelGeometryMixin(GenericPDELabGeometryMixin):
    def define_unit_outer_normal(self, name):
        # NB: Strictly speaking, this implementation holds for any non-curved intersection.
        preamble_normal(name)
        globalarg(name, shape=(world_dimension(),))

    def jacobian_inverse(self, o):
        i, j = self.indices
        assert isinstance(i, int) and isinstance(j, int)

        if i != j:
            self.indices = None
            return 0

        jac = GenericPDELabGeometryMixin.jacobian_inverse(self, o)

        return jac

    def facet_area(self, o):
        # This is not 100% correct, but in practice structured grid implementations are not
        # embedded into higher dimensional world space.
        return self.facet_jacobian_determinant(o)

    def cell_volume(self, o):
        # This is not 100% correct, but in practice structured grid implementations are not
        # embedded into higher dimensional world space.
        return self.jacobian_determinant(o)

    def define_facet_jacobian_determinant(self, name):
        valuearg(name)
        self._define_facet_jacobian_determinant(name)

    @preamble
    def _define_facet_jacobian_determinant(self, name):
        # NB: In the equidistant case, this might be optimized to store *d* values on the operator level
        #     We don't do that right now for laziness.
        geo = name_geometry()
        pos = name_localcenter()

        return "auto {} = {}.integrationElement({});".format(name,
                                                             geo,
                                                             pos,
                                                             )


@geometry_mixin("equidistant")
class EquidistantGeometryMixin(AxiparallelGeometryMixin):
    def define_jacobian_determinant(self, name):
        valuearg(name)
        self._define_jacobian_determinant(name)

    @class_member(classtag="operator")
    def _define_jacobian_determinant(self, name):
        from dune.codegen.pdelab.localoperator import lop_template_ansatz_gfs
        gfst = lop_template_ansatz_gfs()
        self._define_jacobian_determinant_eval(name)
        return "typename {}::Traits::GridView::template Codim<0>::Geometry::ctype {};".format(gfst, name)

    @preamble(kernel="operator")
    def _define_jacobian_determinant_eval(self, name):
        from dune.codegen.pdelab.localoperator import name_ansatz_gfs_constructor_param
        gfs = name_ansatz_gfs_constructor_param()
        rft = type_floatingpoint()
        return "{} = {}.gridView().template begin<0>()->geometry().integrationElement(Dune::FieldVector<{}, {}>());".format(name, gfs, rft, world_dimension())

    def define_jacobian_inverse_transposed(self, name, restriction):
        dim = world_dimension()
        globalarg(name, shape=(dim, dim), managed=False)
        self._define_jacobian_inverse_transposed(name, restriction)

    @class_member(classtag="operator")
    def _define_jacobian_inverse_transposed(self, name, restriction):
        dim = world_dimension()
        self._define_jacobian_inverse_transposed_eval(name)
        from dune.codegen.pdelab.localoperator import lop_template_ansatz_gfs
        gfst = lop_template_ansatz_gfs()
        return "typename {}::Traits::GridView::template Codim<0>::Geometry::JacobianInverseTransposed {};".format(gfst, name)

    @preamble(kernel="operator")
    def _define_jacobian_inverse_transposed_eval(self, name):
        from dune.codegen.pdelab.localoperator import name_ansatz_gfs_constructor_param
        gfs = name_ansatz_gfs_constructor_param()
        rft = type_floatingpoint()
        return "{} = {}.gridView().template begin<0>()->geometry().jacobianInverseTransposed(Dune::FieldVector<{}, {}>());".format(name, gfs, rft, world_dimension())


def enforce_boundary_restriction(visitor):
    if visitor.measure == 'exterior_facet' and visitor.restriction == Restriction.NONE:
        return Restriction.POSITIVE
    else:
        return visitor.restriction


@preamble
def define_reference_element(name):
    geo = name_geometry()
    include_file("dune/geometry/referenceelements.hh", filetag="operatorfile")
    return "auto {} = referenceElement({});".format(name, geo)


def name_reference_element():
    name = "refElement"
    define_reference_element(name)
    return name


@preamble
def define_localcenter(name):
    reference_element = name_reference_element()
    # Note: position(i,c) stands for the barycenter of the i-th subentity of codimension c"
    return "auto {} = {}.position(0,0);".format(name, reference_element)


def name_localcenter():
    name = "localcenter"
    define_localcenter(name)
    return name


@iname
def _component_iname(context, count):
    if context:
        context = '_' + context
    name = 'idim{}{}'.format(context, str(count))
    dim = world_dimension()
    domain(name, dim)
    return name


def component_iname(context='', count=0):
    return _component_iname(context, count)


def name_element_geometry_wrapper():
    return 'eg'


def type_element_geometry_wrapper():
    return 'EG'


def name_intersection_geometry_wrapper():
    return 'ig'


def type_intersection_geometry_wrapper():
    return 'IG'


def name_geometry_wrapper():
    """ Selects the 'native' geometry wrapper of the kernel """
    from dune.codegen.generation import get_global_context_value
    it = get_global_context_value("integral_type")

    if it == 'cell':
        return name_element_geometry_wrapper()
    if it == 'exterior_facet' or it == 'interior_facet':
        return name_intersection_geometry_wrapper()
    assert False


def type_geometry_wrapper():
    """ Selects the 'native' geometry wrapper of the kernel """
    from dune.codegen.generation import get_global_context_value
    it = get_global_context_value("integral_type")

    if it == 'cell':
        return type_element_geometry_wrapper()
    if it == 'exterior_facet' or it == 'interior_facet':
        return type_intersection_geometry_wrapper()
    assert False


@preamble
def define_restricted_cell(name, restriction):
    ig = name_intersection_geometry_wrapper()
    which = "inside" if restriction == Restriction.POSITIVE else "outside"
    return "const auto& {} = {}.{}();".format(name,
                                              ig,
                                              which,
                                              )


def name_cell(restriction):
    if restriction == Restriction.NONE:
        eg = name_element_geometry_wrapper()
        return "{}.entity()".format(eg)
    else:
        which = "inside" if restriction == Restriction.POSITIVE else "outside"
        name = "{}_cell".format(which)
        define_restricted_cell(name, restriction)
        return name


@preamble
def define_cell_geometry(name, restriction):
    cell = name_cell(restriction)
    return "auto {} = {}.geometry();".format(name,
                                             cell
                                             )


def name_cell_geometry(restriction):
    name = restricted_name("cell_geo", restriction)
    define_cell_geometry(name, restriction)
    return name


def type_cell_geometry(restriction):
    if restriction == Restriction.NONE:
        eg = type_element_geometry_wrapper()
        return "{}::Geometry".format(eg)
    else:
        ig = type_intersection_geometry_wrapper()
        return "{}::Entity::Geometry".format(ig)


@preamble
def define_intersection_geometry(name):
    ig = name_intersection_geometry_wrapper()
    return "auto {} = {}.geometry();".format(name,
                                             ig,
                                             )


def name_intersection_geometry():
    define_intersection_geometry("is_geo")
    return "is_geo"


def name_intersection():
    ig = name_intersection_geometry_wrapper()
    return "{}.intersection()".format(ig)


def name_geometry():
    """ Selects the 'native' geometry of the kernel """
    from dune.codegen.generation import get_global_context_value
    it = get_global_context_value("integral_type")

    if it == 'cell':
        return name_cell_geometry(Restriction.NONE)
    if it == 'exterior_facet' or it == 'interior_facet':
        return name_intersection_geometry()
    assert False


@preamble
def define_in_cell_geometry(restriction, name):
    ig = name_intersection_geometry_wrapper()
    which = "In" if restriction == Restriction.POSITIVE else "Out"
    return "auto {} = {}.geometryIn{}side();".format(name,
                                                     ig,
                                                     which
                                                     )


def name_in_cell_geometry(restriction):
    assert restriction is not Restriction.NONE

    name = "geo_in_{}side".format("in" if restriction is Restriction.POSITIVE else "out")
    define_in_cell_geometry(restriction, name)
    return name


@memoize
def world_dimension():
    data = get_global_context_value("data")
    form = data.object_by_name[get_form_option("form")]
    from dune.codegen.ufl.preprocess import preprocess_form
    form = preprocess_form(form).preprocessed_form
    return form.ufl_cell().geometric_dimension()


def intersection_dimension():
    return world_dimension() - 1


def local_dimension():
    it = get_global_context_value('integral_type')
    if it == "cell":
        return world_dimension()
    else:
        return intersection_dimension()


def declare_normal(name, kernel, decl_info):
    ig = name_intersection_geometry_wrapper()
    return "auto {} = {}.centerUnitOuterNormal();".format(name, ig)


@preamble
def preamble_normal(name):
    return declare_normal(name, None, None)


def type_jacobian_inverse_transposed(restriction):
    geo = type_cell_geometry(restriction)
    return "typename {}::JacobianInverseTransposed".format(geo)
