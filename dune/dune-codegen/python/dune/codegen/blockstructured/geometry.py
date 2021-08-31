import pymbolic.primitives as prim
from loopy.match import Writes

from dune.codegen.blockstructured.tools import name_point_in_macro, remove_sub_element_inames
from dune.codegen.generation import (geometry_mixin,
                                     temporary_variable,
                                     instruction,
                                     get_global_context_value,
                                     domain, kernel_cached)
from dune.codegen.loopy.symbolic import FusedMultiplyAdd as FMA
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.geometry import (AxiparallelGeometryMixin,
                                          EquidistantGeometryMixin,
                                          GenericPDELabGeometryMixin,
                                          world_dimension,
                                          local_dimension,
                                          component_iname,
                                          enforce_boundary_restriction,
                                          restricted_name,
                                          name_cell_geometry, name_in_cell_geometry, name_intersection_geometry_wrapper
                                          )
from dune.codegen.pdelab.tensors import name_matrix_inverse, name_determinant
from dune.codegen.tools import get_pymbolic_basename
from dune.codegen.ufl.modified_terminals import Restriction

import numpy as np


@geometry_mixin("blockstructured_multilinear")
class BlockStructuredGeometryMixin(GenericPDELabGeometryMixin):
    def spatial_coordinate(self, o):
        if self.measure == 'cell':
            return self.to_global(self.quadrature_position_in_macro())
        else:
            assert self.measure == 'exterior_facet' or self.measure == 'interior_facet'
            micro_qp = self.to_cell(self.quadrature_position_in_micro())

            macro_qp = prim.Variable(name_point_in_macro(micro_qp, self), )

            return self.to_global(macro_qp)

    def to_global(self, local):
        assert isinstance(local, prim.Expression)
        name = get_pymbolic_basename(local) + "_global"

        # TODO need to assert somehow that local is of codim 0
        compute_multilinear_to_global_transformation(name, local, self)
        return prim.Variable(name)

    def to_cell(self, local):
        assert isinstance(local, prim.Expression)

        restriction = enforce_boundary_restriction(self)
        if restriction == Restriction.NONE:
            return local
        else:
            return self._intersection_to_cell(local, restriction)

    @kernel_cached
    def _intersection_to_cell(self, local, restriction):
        basename = get_pymbolic_basename(local)
        name = "{}_in_{}side".format(basename, "in" if restriction is Restriction.POSITIVE else "out")
        temporary_variable(name, shape=(world_dimension(),), shape_impl=("fv",))
        geo = name_in_cell_geometry(restriction)
        inames = self.quadrature_inames() if get_form_option("blockstructured_prioritize_quad_loop") else\
            remove_sub_element_inames(self.quadrature_inames())
        instruction("{} = {}.global({});".format(name, geo, str(local)),
                    assignees=frozenset({name}),
                    read_variables=frozenset({get_pymbolic_basename(local)}),
                    depends_on=frozenset({Writes(get_pymbolic_basename(local))}),
                    within_inames=frozenset(inames)
                    )

        return prim.Variable(name)

    def facet_jacobian_determinant(self, o):
        return prim.Product((GenericPDELabGeometryMixin.facet_jacobian_determinant(self, o),
                             1 / (get_form_option("number_of_blocks") ** local_dimension())))

    def jacobian_determinant(self, o):
        jacobian = name_jacobian_matrix(self)
        name = name_determinant(jacobian, (world_dimension(), world_dimension()), self)

        return prim.Product((prim.Call(prim.Variable("abs"), (prim.Variable(name),)),
                             1 / (get_form_option("number_of_blocks") ** local_dimension())))

    def jacobian_inverse(self, o):
        assert(len(self.indices) == 2)
        i, j = self.indices
        self.indices = None

        restriction = enforce_boundary_restriction(self)

        jacobian = restricted_name(name_jacobian_matrix(self), restriction)
        name = name_matrix_inverse(jacobian, (world_dimension(), world_dimension()), self)

        return prim.Product((prim.Subscript(prim.Variable(name), (j, i)),
                             get_form_option("number_of_blocks")))


@geometry_mixin("blockstructured_axiparallel")
class AxiparallelBlockStructuredGeometryMixin(AxiparallelGeometryMixin, BlockStructuredGeometryMixin):
    def to_global(self, local):
        assert isinstance(local, prim.Expression)
        name = get_pymbolic_basename(local) + "_global"

        # TODO need to assert somehow that local is of codim 0
        compute_axiparallel_to_global_transformation(name, local, self)
        return prim.Variable(name)

    def jacobian_determinant(self, o):
        return prim.Product((AxiparallelGeometryMixin.jacobian_determinant(self, o),
                             1 / (get_form_option("number_of_blocks") ** local_dimension())))

    def jacobian_inverse(self, o):
        return prim.Product((AxiparallelGeometryMixin.jacobian_inverse(self, o),
                             get_form_option("number_of_blocks")))


@geometry_mixin("blockstructured_equidistant")
class EquidistantBlockStructuredGeometryMixin(EquidistantGeometryMixin, AxiparallelBlockStructuredGeometryMixin):
    pass


# TODO warum muss within_inames_is_final=True gesetzt werden?
def compute_corner_diff(first, second, additional_terms=tuple()):
    corners = name_element_corners()
    simplified_names = tuple("cd" + n.split('_')[2] + n.split('_')[3] for n in additional_terms)
    name = "corner_diff_" + "_".join((str(first), str(second)) + simplified_names)
    temporary_variable(name, shape_impl=('fv',), shape=(world_dimension(),))
    diminame = component_iname(context='corner')

    if additional_terms:
        xs_sum = prim.Sum(tuple(prim.Subscript(prim.Variable(x), (prim.Variable(diminame),)) for x in additional_terms))
    else:
        xs_sum = 0

    instruction(expression=prim.Sum((prim.Subscript(prim.Variable(corners), (first, prim.Variable(diminame))),
                                     -1 * prim.Subscript(prim.Variable(corners), (second, prim.Variable(diminame))),
                                     -1 * xs_sum)),
                assignee=prim.Subscript(prim.Variable(name), prim.Variable(diminame)),
                within_inames=frozenset({diminame}),
                within_inames_is_final=True,
                depends_on=frozenset({Writes(corners)} | {Writes(term) for term in additional_terms}))
    return name


# Compute the coefficients for the bilinear geometry transformation
def bilinear_transformation_coefficients():
    dim = world_dimension()
    if dim == 2:
        # Transformation T(x,y) = a * xy + b * x + c * y + d
        c = compute_corner_diff(2, 0)
        b = compute_corner_diff(1, 0)
        a = compute_corner_diff(3, 0, (b, c))
        return [a, b, c]
    elif dim == 3:
        # Transformation T(x,y,z) = a * xyz + b * xy + c * xz + d * yz + e * x + f * y + g * z + h
        g = compute_corner_diff(4, 0)
        f = compute_corner_diff(2, 0)
        e = compute_corner_diff(1, 0)
        d = compute_corner_diff(6, 0, (f, g))
        c = compute_corner_diff(5, 0, (e, g))
        b = compute_corner_diff(3, 0, (e, f))
        a = compute_corner_diff(7, 0, (b, c, d, e, f, g))
        return [a, b, c, d, e, f, g]
    else:
        raise NotImplementedError()


def compute_jacobian(name, visitor):
    pymbolic_pos = visitor.quadrature_position_in_macro()
    jac_iname = component_iname(context="jac")

    coefficients = bilinear_transformation_coefficients()

    if world_dimension() == 2:
        a, b, c = coefficients

        expr_jac = [None, None]
        expr_jac[0] = FMA(prim.Subscript(pymbolic_pos, (1,)),
                          prim.Subscript(prim.Variable(a), (prim.Variable(jac_iname),)),
                          prim.Subscript(prim.Variable(b), (prim.Variable(jac_iname),)))
        expr_jac[1] = FMA(prim.Subscript(pymbolic_pos, (0,)),
                          prim.Subscript(prim.Variable(a), (prim.Variable(jac_iname),)),
                          prim.Subscript(prim.Variable(c), (prim.Variable(jac_iname),)))
    elif world_dimension() == 3:
        a, b, c, d, e, f, g = coefficients

        expr_jac = [None, None, None]
        terms = [[b, c, e], [b, d, f], [c, d, g]]

        # j[:][i] = a * qp[k]*qp[l] + v1 * qp[k] + v2 * qp[l] + v3
        # with k, l in {0,1,2} != i and k<l and vj = terms[i][j]
        for i in range(3):
            k, l = sorted(set(range(3)) - {i})
            expr_jac[i] = FMA(prim.Subscript(prim.Variable(a), (prim.Variable(jac_iname),)),
                              prim.Subscript(pymbolic_pos, (k,)) * prim.Subscript(pymbolic_pos, (l,)),
                              FMA(prim.Subscript(prim.Variable(terms[i][0]), (prim.Variable(jac_iname),)),
                                  prim.Subscript(pymbolic_pos, (k,)),
                                  FMA(prim.Subscript(prim.Variable(terms[i][1]), (prim.Variable(jac_iname),)),
                                      prim.Subscript(pymbolic_pos, (l,)),
                                      prim.Subscript(prim.Variable(terms[i][2]), (prim.Variable(jac_iname),)))))
    else:
        raise NotImplementedError()

    for i, expr in enumerate(expr_jac):
        instruction(expression=expr,
                    assignee=prim.Subscript(prim.Variable(name), (prim.Variable(jac_iname), i)),
                    within_inames=frozenset((jac_iname, ) + visitor.quadrature_inames()),
                    depends_on=frozenset({Writes(get_pymbolic_basename(pymbolic_pos))} | {Writes(cd) for cd in coefficients})
                    )


def define_jacobian_matrix(name, visitor):
    temporary_variable(name, shape=(world_dimension(), world_dimension()), managed=True)
    compute_jacobian(name, visitor)


def name_jacobian_matrix(visitor):
    name = "jacobian"
    define_jacobian_matrix(name, visitor)
    return name


def compute_multilinear_to_global_transformation(name, local, visitor):
    dim = world_dimension()
    temporary_variable(name, shape=(dim,), managed=True)
    corners = name_element_corners()

    if isinstance(local, str):
        local = prim.Variable(local)

    dim_pym = prim.Variable(component_iname('to_global'))

    coeffs_pym = [prim.Subscript(prim.Variable(coeff), (dim_pym,)) for coeff in bilinear_transformation_coefficients()]

    local_pym = [prim.Subscript(local, i) for i in range(dim)]

    corner_0_pym = prim.Subscript(prim.Variable(corners), (0, dim_pym))

    # global[d] = T(local)[d]
    if dim == 2:
        a_pym, b_pym, c_pym = coeffs_pym
        expr = FMA(a_pym, local_pym[0] * local_pym[1], FMA(b_pym, local_pym[0], FMA(c_pym, local_pym[1], corner_0_pym)))
    elif dim == 3:
        a_pym, b_pym, c_pym, d_pym, e_pym, f_pym, g_pym = coeffs_pym
        expr = FMA(a_pym * local_pym[0], local_pym[1] * local_pym[2],
                   FMA(b_pym, local_pym[0] * local_pym[1],
                       FMA(c_pym, local_pym[0] * local_pym[2],
                           FMA(d_pym, local_pym[1] * local_pym[2],
                               FMA(e_pym, local_pym[0],
                                   FMA(f_pym, local_pym[1], FMA(g_pym, local_pym[2], corner_0_pym)))))))
    else:
        raise NotImplementedError

    assignee = prim.Subscript(prim.Variable(name), (dim_pym,))

    instruction(assignee=assignee, expression=expr,
                within_inames=frozenset(visitor.quadrature_inames() + (dim_pym.name,)),
                within_inames_is_final=True,
                depends_on=frozenset({Writes(get_pymbolic_basename(local)), Writes(corners)})
                )


def compute_axiparallel_to_global_transformation(name, local, visitor):
    dim = world_dimension()
    temporary_variable(name, shape=(dim,), managed=True)
    corners = name_element_corners()

    if isinstance(local, str):
        local = prim.Variable(local)

    dim_pym = prim.Variable(component_iname('to_global'))

    # global[d] = lower_left[d] + local[d] * (upper_right[d] - lower_left[d])
    expr = FMA(prim.Subscript(prim.Variable(corners), (2**dim - 1, dim_pym)) -
               prim.Subscript(prim.Variable(corners), (0, dim_pym)),
               prim.Subscript(local, (dim_pym,)), prim.Subscript(prim.Variable(corners), (0, dim_pym)))

    assignee = prim.Subscript(prim.Variable(name), (dim_pym,))

    instruction(assignee=assignee, expression=expr,
                within_inames=frozenset(visitor.quadrature_inames() + (dim_pym.name,)),
                within_inames_is_final=True,
                depends_on=frozenset({Writes(get_pymbolic_basename(local)), Writes(corners)})
                )


def define_element_corners(name):
    from dune.codegen.pdelab.driver import get_form
    n_corners = get_form().ufl_cell().num_vertices()
    temporary_variable(name, shape_impl=('fv', 'fv'), shape=(n_corners, world_dimension()))

    iname = "i_corner"
    domain(iname, n_corners)

    it = get_global_context_value("integral_type")
    if it == 'cell':
        restriction = Restriction.NONE
    elif it == 'exterior_facet':
        restriction = Restriction.POSITIVE
    else:
        raise NotImplementedError()

    instruction(code="{}[{}] = {}.corner({});".format(name, iname, name_cell_geometry(restriction), iname),
                assignees=frozenset({prim.Subscript(prim.Variable(name), (prim.Variable(iname), 0))}),
                within_inames=frozenset({iname}), within_inames_is_final=True)


def name_element_corners():
    name = "corners"
    define_element_corners(name)
    return name


def name_face_id(restriction):
    pdelab_name = {Restriction.POSITIVE: "inside",
                   Restriction.NEGATIVE: "outside"}

    face_id = "face_id"
    temporary_variable(face_id, shape=(), dtype=np.int32)
    instruction(code="{} = {}.indexIn{}();".format(face_id, name_intersection_geometry_wrapper(),
                                                   pdelab_name[restriction].capitalize()),
                assignees=(face_id,))
    return face_id
