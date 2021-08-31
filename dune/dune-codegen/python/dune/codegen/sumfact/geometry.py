""" Sum factorized geometry evaluations """

from dune.codegen.generation import (class_member,
                                     domain,
                                     geometry_mixin,
                                     get_counted_variable,
                                     iname,
                                     include_file,
                                     instruction,
                                     kernel_cached,
                                     preamble,
                                     silenced_warning,
                                     temporary_variable,
                                     get_global_context_value,
                                     globalarg,
                                     valuearg,
                                     )
from dune.codegen.loopy.flatten import flatten_index
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.options import get_form_option, get_option
from dune.codegen.pdelab.geometry import (enforce_boundary_restriction,
                                          local_dimension,
                                          world_dimension,
                                          name_cell_geometry,
                                          name_geometry,
                                          GenericPDELabGeometryMixin,
                                          AxiparallelGeometryMixin,
                                          EquidistantGeometryMixin,
                                          )
from dune.codegen.pdelab.localoperator import (name_ansatz_gfs_constructor_param,
                                               lop_template_ansatz_gfs,
                                               )
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.sumfact.accumulation import basis_sf_kernels, sumfact_iname
from dune.codegen.sumfact.basis import construct_basis_matrix_sequence
from dune.codegen.sumfact.permutation import (permute_backward,
                                              permute_forward,
                                              sumfact_cost_permutation_strategy,
                                              sumfact_quadrature_permutation_strategy,
                                              )
from dune.codegen.sumfact.quadrature import additional_inames
from dune.codegen.sumfact.symbolic import SumfactKernelInterfaceBase, SumfactKernel
from dune.codegen.tools import get_pymbolic_basename, ImmutableCuttingRecord
from dune.codegen.ufl.modified_terminals import Restriction

from loopy.match import Writes

import pymbolic.primitives as prim
import numpy as np
import loopy as lp


class SumfactGeometryMixinBase(GenericPDELabGeometryMixin):
    def nonsumfact_fallback(self):
        return None


@geometry_mixin("sumfact_multilinear")
class SumfactMultiLinearGeometryMixin(SumfactGeometryMixinBase):
    def nonsumfact_fallback(self):
        return "generic"

    def _jacobian_inverse(self):
        return "jit"

    def jacobian_inverse(self, o):
        # This differs from the generic one by not falling back to the
        # transpose of the jacobian inverse.
        restriction = enforce_boundary_restriction(self)

        assert(len(self.indices) == 2)
        i, j = self.indices
        self.indices = None

        name = restricted_name(self._jacobian_inverse(), restriction)
        self.define_jacobian_inverse(name, restriction)

        return prim.Subscript(prim.Variable(name), (i, j))

    def _jacobian_determinant(self):
        return "detjac"

    def define_jacobian_determinant(self, o):
        restriction = Restriction.NONE if self.measure == "cell" else Restriction.POSITIVE
        self.define_jacobian_inverse(self._jacobian_inverse(), restriction)
        return prim.Variable(self._jacobian_determinant())

    def define_jacobian_inverse(self, name, restriction):
        """Return jacobian inverse of the geometry mapping (of a cell)

        At the moment this only works for geometry mappings of cells and not for
        intersection. We only consider this case as it greatly simplifies code
        generation for unstructured grids by making the grid edge consistent and
        avoiding the face-twist problem.
        """
        # Calculate the jacobian of the geometry mapping using sum factorization
        dim = world_dimension()
        names_jacobian = []
        for j in range(dim):
            for i in range(dim):
                name_jacobian = restricted_name("jacobian_geometry_{}{}".format(i, j), restriction)
                temporary_variable(name_jacobian)
                assignee = prim.Variable(name_jacobian)
                expression = _name_jacobian(i, j, restriction, self)
                inames = self.quadrature_inames() + additional_inames(self)
                instruction(assignee=assignee,
                            expression=expression,
                            within_inames=frozenset(inames),
                            depends_on=frozenset({lp.match.Tagged("sumfact_stage1")}),
                            tags=frozenset({"sumfact_stage2"}),
                            no_sync_with=frozenset({(lp.match.Tagged("sumfact_stage2"), "any")})
                            )
                names_jacobian.append(name_jacobian)

                # The sum factorization kernels from the geometry evaluation of the
                # jacobians will never appear in the expression for the input of
                # stage 3. This way the SumfactCollectMapper will never see them
                # and they will be marked as inactive. Here we explicitly mark the
                # as used.
                basis_sf_kernels(expression.aggregate)

        # Calculate the inverse of the jacobian of the geometry mapping and the
        # determinant by calling a c++ function. Note: The result will be column
        # major -> fortran style.
        name_detjac = self._jacobian_determinant()
        temporary_variable(name_detjac, shape=())
        ftags = "f,f"
        temporary_variable(name, shape=(dim, dim), dim_tags=ftags, managed=True)
        include_file('dune/codegen/sumfact/invertgeometry.hh', filetag='operatorfile')
        code = "{} = invert_and_return_determinant({}, {});".format(name_detjac,
                                                                    ", ".join(names_jacobian),
                                                                    name)
        silenced_warning("read_no_write({})".format(name_detjac))
        inames = self.quadrature_inames() + additional_inames(self)
        return instruction(code=code,
                           assignees=frozenset([name, name_detjac]),
                           read_variables=frozenset(names_jacobian),
                           inames=frozenset(inames),
                           tags=frozenset({"sumfact_stage2"}),
                           no_sync_with=frozenset({(lp.match.Tagged("sumfact_stage2"), "any")})
                           )

    def facet_jacobian_determinant(self, o):
        """Absolute value of determinant of jacobian of facet geometry mapping

        Calculate the absolute value of the determinant of the jacobian of the
        geometry mapping from the reference cell of the intersection to the
        intersection:

        |\det(\nabla \mu_F)|

        This is done using the surface metric tensor lemma from the lecture notes
        of Jean-Luc Guermond:

        |\det(\nabla \mu_F)| = \| \tilde{n} \| |\det(\nabla \mu_{T_s})|

        Here \tilde{n} is the outer normal defined by:

        \tilde{n} = (\nabla \mu_{T_s})^{-T} \hat{n}_s

        where \hat{n}_s is the unit outer normal of the corresponding face of the
        reference cell.
        """
        detjac = self.jacobian_determinant(None)
        norm_of_outer_normal = normalize(self.outer_normal(), world_dimension())

        return prim.Product((detjac, norm_of_outer_normal))

    def outer_normal(self):
        """ This is the *unnormalized* outer normal """
        name = "outer_normal"
        facedir_s = self.get_facedir(Restriction.POSITIVE)
        facemod_s = self.get_facemod(Restriction.POSITIVE)

        temporary_variable(name, shape=(world_dimension(),))
        for i in range(world_dimension()):
            assignee = prim.Subscript(prim.Variable(name), i)
            self.indices = (facedir_s, i)
            ji = self.jacobian_inverse(None)

            # Note: 2*facemod_s-1 because of
            # -1 if facemod_s = 0
            # +1 if facemod_s = 1
            expression = ji * (2 * facemod_s - 1)

            inames = self.quadrature_inames() + additional_inames(self)
            instruction(assignee=assignee,
                        expression=expression,
                        within_inames=frozenset(inames),
                        )

        return prim.Variable(name)

    def facet_normal(self, o):
        index, = self.indices
        self.indices = None

        outer_normal = self.outer_normal()
        norm = normalize(outer_normal, world_dimension())

        return prim.Subscript(outer_normal, (index,)) / norm

    def spatial_coordinate(self, o):
        """Calculate global coordinates of quadrature points for multilinear geometry mappings

        The evalualation is done using sum factorization techniques.

        On facets we use the geometry mapping of the self cell to get a global
        evaluation of the quadrature points. Avoiding the geometry mapping of the
        face itself greatly simplifies the generation of code for unstructured
        grids. Instead of looking at all the possible embeddings of the reference
        element of the face into the reference element of the cell we can make the
        grid edge consistent and choose a suitable convention for the order of
        directions in our sum factorization kernels.
        """
        assert len(self.indices) == 1
        restriction = enforce_boundary_restriction(self)

        # Generate sum factorization kernel and add vectorization info
        matrix_sequence = construct_basis_matrix_sequence(facedir=self.get_facedir(restriction),
                                                          facemod=self.get_facemod(restriction),
                                                          basis_size=(2,) * world_dimension())
        inp = GeoCornersInput(matrix_sequence=matrix_sequence,
                              direction=self.indices[0],
                              restriction=restriction,
                              )
        sf = SumfactKernel(matrix_sequence=matrix_sequence,
                           interface=inp,
                           )

        from dune.codegen.sumfact.vectorization import attach_vectorization_info
        vsf = attach_vectorization_info(sf)

        # If this sum factorization kernel was not used in the dry run we
        # just return 0
        if vsf == 0:
            self.indices = None
            return 0

        # Add a sum factorization kernel that implements the evaluation of
        # the basis functions at quadrature points (stage 1)
        from dune.codegen.sumfact.realization import realize_sum_factorization_kernel
        var, _ = realize_sum_factorization_kernel(vsf)

        # The results of this function is already the right component of the
        # spatial coordinate and we don't need to index this in the visitor
        self.indices = None

        return prim.Subscript(var, vsf.quadrature_index(sf, self))


@geometry_mixin("sumfact_axiparallel")
class SumfactAxiParallelGeometryMixin(SumfactGeometryMixinBase, AxiparallelGeometryMixin):
    def nonsumfact_fallback(self):
        return "axiparallel"

    def facet_normal(self, o):
        i, = self.indices
        self.indices = None
        assert isinstance(i, int)

        # Use facemod_s and facedir_s
        if i == self.get_facedir(Restriction.POSITIVE):
            if self.get_facemod(Restriction.POSITIVE):
                return 1
            else:
                return -1
        else:
            return 0


@geometry_mixin("sumfact_equidistant")
class SumfactEqudistantGeometryMixin(EquidistantGeometryMixin, SumfactAxiParallelGeometryMixin):
    def nonsumfact_fallback(self):
        return "equidistant"

    def facet_jacobian_determinant(self, o):
        name = "fdetjac"
        self.define_facet_jacobian_determinant(name)
        facedir = self.get_facedir(Restriction.POSITIVE)
        globalarg(name, shape=(world_dimension(),))
        return prim.Subscript(prim.Variable(name), (facedir,))

    @class_member(classtag="operator")
    def define_facet_jacobian_determinant(self, name):
        self._define_facet_jacobian_determinant_eval(name)
        gfst = lop_template_ansatz_gfs()
        return "std::array<typename {}::Traits::GridView::template Codim<0>::Geometry::ctype, {}> {};".format(gfst, world_dimension(), name)

    @kernel_cached(kernel="operator")
    def _define_facet_jacobian_determinant_eval(self, name):
        gfs = name_ansatz_gfs_constructor_param()
        rft = type_floatingpoint()
        code = ["{",
                "  auto e = *({}.gridView().template begin<0>());".format(gfs),
                "  int dir=0;",
                "  for(auto is = {0}.gridView().ibegin(e); is != {0}.gridView().iend(e); ++(++is), ++dir)".format(gfs),
                "    {}[dir] = is->geometry().integrationElement(Dune::FieldVector<{}, {}>());".format(name, rft, world_dimension() - 1),
                "}",
                ]
        instruction(code="\n".join(code),
                    kernel="operator",
                    )

    def spatial_coordinate(self, o):
        index, = self.indices

        # Urgh: *SOMEHOW* construct a face direction. This is not breaking in the unstructured
        # case, because we do not enter this code path...
        from dune.codegen.pdelab.restriction import Restriction
        restriction = Restriction.NONE
        if self.measure == "interior_facet":
            restriction = Restriction.POSITIVE
        face = self.get_facedir(restriction)

        lowcorner = name_lowerleft_corner()
        meshwidth = name_meshwidth()

        # If we have to decide which boundary condition to take for this
        # intersection we always take the boundary condition of the center
        # of the intersection. We assume that there are no cells with more
        # than one boundary condition.
        if self.do_predicates:
            x = 0.5
        elif index == face:
            x = 0
        else:
            iindex = index
            if face is not None and index > face:
                iindex = iindex - 1
            x = self.quadrature_position(iindex)

        self.indices = None
        return prim.Subscript(prim.Variable(lowcorner), (index,)) + x * prim.Subscript(prim.Variable(meshwidth), (index,))


@iname
def global_corner_iname(restriction):
    name = get_counted_variable(restricted_name("global_corneriname", restriction))
    domain(name, 2 ** world_dimension())
    return name


class GeoCornersInput(SumfactKernelInterfaceBase, ImmutableCuttingRecord):
    def __init__(self,
                 matrix_sequence=None,
                 direction=None,
                 restriction=None):
        """Base class for sum-factorized evaluation of geometry mappings

        At the moment we only do this for cells and not faces. For
        intersections we do this corresponding reference elements of the
        neigboring cells.

        Each spatial component needs a seperate sum factorization kernel.  The
        argument 'direction' specifies the component (x-component: 0,
        y-component: 1, z-component: 2).
        """

        # Note: The function sumfact_quadrature_permutation_strategy does not
        # work anymore after the visiting process since get_facedir and
        # get_facemod are not well defined. But we need the
        # quadrature_permutation to generate the name of the sumfact
        # kernel. This means we need to store the value here instead of
        # recalculating it in the property.
        dim = world_dimension()
        quadrature_permutation = sumfact_quadrature_permutation_strategy(dim, restriction)
        matrix_sequence = permute_forward(matrix_sequence, quadrature_permutation)

        # Note: Do not put matrix_sequence into the Record. That screws up the vectorization strategy!
        ImmutableCuttingRecord.__init__(self,
                                        direction=direction,
                                        restriction=restriction,
                                        _quadrature_permutation=quadrature_permutation,
                                        _permuted_matrix_sequence=matrix_sequence,
                                        )

    def get_keyword_arguments(self):
        """Get dictionary of keyword arguments needed to initialize this class

        Extract keyword arguments from the ImmutableRecord and modify
        accordingly. You need to set the correct matrix sequence before using
        this dict to create an interface.
        """
        dict = self.get_copy_kwargs()
        del dict['_permuted_matrix_sequence']
        del dict['_quadrature_permutation']
        dict['matrix_sequence'] = None
        return dict

    @property
    def quadrature_permutation(self):
        return self._quadrature_permutation

    @property
    def cost_permutation(self):
        return sumfact_cost_permutation_strategy(self._permuted_matrix_sequence, self.stage)

    @property
    def stage(self):
        return 1

    @property
    def direct_is_possible(self):
        return False

    def setup_input(self, sf, insn_dep, index=0):
        # Inames for interating over the coefficients (in this case the
        # coordinate of the component 'sefl.direction' of the corners). We take
        # them from the cost permuted matrix sequence. In order to get the
        # inames in order x,y,... we need to take the permutation back.
        shape_cost_permuted = tuple(mat.basis_size for mat in sf.matrix_sequence_cost_permuted)
        shape_ordered = permute_backward(shape_cost_permuted, self.cost_permutation)
        shape_ordered = permute_backward(shape_ordered, self.quadrature_permutation)
        inames_cost_permuted = tuple(sumfact_iname(length, "corner_setup_inames_" + str(k)) for k, length in enumerate(shape_cost_permuted))
        inames_ordered = permute_backward(inames_cost_permuted, self.cost_permutation)
        inames_ordered = permute_backward(inames_ordered, self.quadrature_permutation)

        # Flat indices needed to access pdelab corner method
        flat_index_ordered = flatten_index(tuple(prim.Variable(i) for i in inames_ordered),
                                           shape_ordered,
                                           order="f")
        flat_index_cost_permuted = flatten_index(tuple(prim.Variable(i) for i in inames_cost_permuted),
                                                 shape_cost_permuted,
                                                 order="f")

        # The array that will be passed to the sum factorization kernel
        # function should contain the coefficients in the cost permuted order!
        from dune.codegen.sumfact.realization import name_buffer_storage
        name = "input_{}".format(sf.buffer)
        ftags = ",".join(["f"] * (sf.length + 1))
        temporary_variable(name,
                           shape=(sf.vector_width,) + shape_cost_permuted,
                           custom_base_storage=name_buffer_storage(sf.buffer, 0),
                           managed=True,
                           dim_tags=ftags,
                           )

        if self.restriction == 0:
            geo = name_geometry()
        else:
            geo = name_cell_geometry(self.restriction)

        # NB: We need to realize this as a C instruction, because the corner
        #     method does return a non-scalar, which does not fit into the current
        #     loopy philosophy for function calls. This problem will be solved once
        #     #11 is resolved. Admittedly, the code looks *really* ugly until that happens.
        code = "{}[{}*({})+{}] = {}.corner({})[{}];".format(name,
                                                            sf.vector_width,
                                                            str(flat_index_cost_permuted),
                                                            index,
                                                            geo,
                                                            str(flat_index_ordered),
                                                            self.direction,
                                                            )

        insn = instruction(code=code,
                           within_inames=frozenset(inames_cost_permuted),
                           assignees=(name,),
                           tags=frozenset({"sumfact_setup", "sumfact_stage{}".format(sf.stage)}),
                           no_sync_with=frozenset({(lp.match.Tagged("sumfact_setup"), "any")})
                           )

        return insn_dep.union(frozenset({insn}))

    def realize_input(self, sf, inames, shape, vec_iname, vec_shape, buf, ftags):
        # Get a temporary that interprets the base storage of the input
        # as a column-major matrix. In later iteration of the matrix loop
        # this reinterprets the output of the previous iteration.
        inp = buf.get_temporary(sf,
                                "buff_step0_in",
                                shape=shape + vec_shape,
                                dim_tags=ftags,
                                )

        # The input temporary will only be read from, so we need to silence
        # the loopy warning
        silenced_warning('read_no_write({})'.format(inp))

        return prim.Subscript(prim.Variable(inp), inames + vec_iname)


@preamble
def define_corner(name, low):
    geo = name_geometry()
    return "auto {} = {}.corner({});".format(name,
                                             geo,
                                             0 if low else 2 ** local_dimension() - 1)


@class_member(classtag="operator")
def define_mesh_width(name):
    rft = type_floatingpoint()
    define_mesh_width_eval(name)
    return "Dune::FieldVector<{}, {}> {};".format(rft, world_dimension(), name)


def define_mesh_width_eval(name):
    from dune.codegen.pdelab.localoperator import name_ansatz_gfs_constructor_param
    gfs = name_ansatz_gfs_constructor_param()
    code = ["{",
            "  auto e = *({}.gridView().template begin<0>());".format(gfs),
            "  {} = e.geometry().corner((1<<{}) - 1);".format(name, world_dimension()),
            "  {} -= e.geometry().corner(0);".format(name),
            "}",
            ]
    instruction(code="\n".join(code),
                kernel="operator")


def name_lowerleft_corner():
    name = "lowerleft_corner"
    globalarg(name, shape=(world_dimension(),))
    define_corner(name, True)
    return name


def name_meshwidth():
    name = "meshwidth"
    globalarg(name, shape=(world_dimension(),))
    define_mesh_width(name)
    return name


@kernel_cached
def _name_jacobian(i, j, restriction, visitor):
    """Return the (i, j) component of the jacobian of the geometry mapping

    Evaluation of the derivative of the geometry mapping is done using sum
    factorization.

    Note: At the moment this only works for the mappings from reference cells
    to the cell and not for the geometry mappings of intersections.
    """
    # Create matrix sequence with derivative in j direction
    matrix_sequence = construct_basis_matrix_sequence(derivative=j,
                                                      facedir=visitor.get_facedir(restriction),
                                                      facemod=visitor.get_facemod(restriction),
                                                      basis_size=(2,) * world_dimension())

    # Sum factorization input for the i'th component of the geometry mapping
    inp = GeoCornersInput(matrix_sequence=matrix_sequence,
                          direction=i,
                          restriction=restriction)
    sf = SumfactKernel(matrix_sequence=matrix_sequence,
                       interface=inp,
                       )
    from dune.codegen.sumfact.vectorization import attach_vectorization_info
    vsf = attach_vectorization_info(sf)

    # If this sum factorization kernel was not used in the dry run we
    # just return 0
    if vsf == 0:
        visitor.indices = None
        return 0

    # Add a sum factorization kernel that implements the evaluation of
    # the basis functions at quadrature points (stage 1)
    from dune.codegen.sumfact.realization import realize_sum_factorization_kernel
    var, _ = realize_sum_factorization_kernel(vsf)

    assert(visitor.indices is None)
    return prim.Subscript(var, vsf.quadrature_index(sf, visitor))


def normalize(expr, dim):
    return prim.Call(prim.Variable("sqrt"), (prim.Sum(tuple(expr[i] * expr[i] for i in range(dim))),))
