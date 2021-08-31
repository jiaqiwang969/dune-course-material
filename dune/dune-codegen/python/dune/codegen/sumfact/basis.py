""" Generator functions to evaluate trial and test functions

NB: Basis evaluation is only needed for the trial function argument in jacobians, as the
multiplication with the test function is part of the sum factorization kernel.
"""
import itertools

from dune.codegen.generation import (basis_mixin,
                                     domain,
                                     get_counted_variable,
                                     get_counter,
                                     get_global_context_value,
                                     globalarg,
                                     iname,
                                     instruction,
                                     kernel_cached,
                                     silenced_warning,
                                     temporary_variable,
                                     )
from dune.codegen.loopy.flatten import flatten_index
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.sumfact.tabulation import (basis_functions_per_direction,
                                             construct_basis_matrix_sequence,
                                             BasisTabulationMatrix,
                                             PolynomialLookup,
                                             name_polynomials,
                                             polynomial_degree,
                                             )
from dune.codegen.sumfact.permutation import (permute_backward,
                                              permute_forward,
                                              sumfact_cost_permutation_strategy,
                                              sumfact_quadrature_permutation_strategy,
                                              )
from dune.codegen.pdelab.argument import name_coefficientcontainer, name_applycontainer
from dune.codegen.pdelab.basis import GenericBasisMixin
from dune.codegen.pdelab.geometry import (local_dimension,
                                          world_dimension,
                                          )
from dune.codegen.sumfact.symbolic import SumfactKernel, SumfactKernelInterfaceBase
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.driver import FEM_name_mangling
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.pdelab.spaces import name_lfs, name_leaf_lfs
from dune.codegen.tools import maybe_wrap_subscript, ImmutableCuttingRecord
from dune.codegen.pdelab.basis import shape_as_pymbolic
from dune.codegen.sumfact.accumulation import sumfact_iname

from ufl import MixedElement, VectorElement, TensorElement, TensorProductElement

from pytools import product

from loopy.match import Writes

import pymbolic.primitives as prim


@basis_mixin("sumfact")
class SumfactBasisMixin(GenericBasisMixin):
    def lfs_inames(self, element, restriction, number=1):
        from ufl import FiniteElement, TensorProductElement
        assert isinstance(element, (FiniteElement, TensorProductElement))
        if number == 0:
            return ()
        else:
            dim = world_dimension()
            return tuple(sumfact_lfs_iname(element, _basis_functions_per_direction(element)[d], d) for d in range(dim))

    def implement_basis(self, element, restriction, number):
        # If this is a test function we omit it!
        if number == 0:
            return 1

        assert not isinstance(element, MixedElement)

        name = "phi_{}".format(FEM_name_mangling(element))
        name = restricted_name(name, restriction)
        self.evaluate_basis(element, name, restriction)

        return prim.Variable(name)

    @kernel_cached
    def evaluate_basis(self, element, name, restriction):
        temporary_variable(name, shape=())
        quad_inames = self.quadrature_inames()
        inames = self.lfs_inames(element, restriction)
        facedir = self.get_facedir(restriction)

        # Collect the pairs of lfs/quad inames that are in use
        # On facets, the normal direction of the facet is excluded
        #
        # If facedir is not none, the length of inames and quad_inames is
        # different. For inames we want to skip the facedir direction, for
        # quad_inames we need all entries. Thats the reason for the
        # help_index.
        basis_per_dir = _basis_functions_per_direction(element)
        prod = ()
        help_index = 0
        for direction in range(len(inames)):
            if direction != facedir:
                prod = prod + (BasisTabulationMatrix(basis_size=basis_per_dir[direction],
                                                     direction=direction).pymbolic((prim.Variable(quad_inames[help_index]), prim.Variable(inames[direction]))),)
                help_index += 1

        # Add the missing direction on facedirs by evaluating at either 0 or 1
        if facedir is not None:
            facemod = self.get_facemod(restriction)
            prod = prod + (prim.Call(PolynomialLookup(name_polynomials(element.degree()), False),
                                     (prim.Variable(inames[facedir]), facemod)),)

        # Issue the product
        instruction(expression=prim.Product(prod),
                    assignee=prim.Variable(name),
                    forced_iname_deps=frozenset(quad_inames + inames),
                    forced_iname_deps_is_final=True,
                    )

    def implement_reference_gradient(self, element, restriction, number):
        # If this is a test function, we omit it.
        if number == 0:
            self.indices = None
            return 1

        assert len(self.indices) == 1
        index, = self.indices

        # TODO: Change name?
        name = "js_{}".format(FEM_name_mangling(element))
        name = restricted_name(name, restriction)
        name = "{}_{}".format(name, index)
        self.evaluate_reference_gradient(element, name, restriction, index)

        self.indices = None
        return prim.Variable(name)

    @kernel_cached
    def evaluate_reference_gradient(self, element, name, restriction, index):
        dim = world_dimension()
        temporary_variable(name, shape=())
        quad_inames = self.quadrature_inames()
        inames = self.lfs_inames(element, restriction)
        facedir = self.get_facedir(restriction)

        # Map the direction to a quadrature iname
        quadinamemapping = {}
        i = 0
        for d in range(local_dimension()):
            if d == facedir:
                i = i + 1
            quadinamemapping[i] = quad_inames[d]
            i = i + 1

        prod = []
        for i in range(dim):
            if i != facedir:
                tab = BasisTabulationMatrix(basis_size=_basis_functions_per_direction(element)[i],
                                            direction=i,
                                            derivative=index == i)
                prod.append(tab.pymbolic((prim.Variable(quadinamemapping[i]), prim.Variable(inames[i]))))

        if facedir is not None:
            facemod = self.get_facemod(restriction)
            prod.append(prim.Call(PolynomialLookup(name_polynomials(element.degree()), index == facedir),
                                  (prim.Variable(inames[facedir]), facemod)),)

        instruction(assignee=prim.Variable(name),
                    expression=prim.Product(tuple(prod)),
                    forced_iname_deps=frozenset(quad_inames + inames),
                    forced_iname_deps_is_final=True,
                    )

    def implement_trialfunction(self, element, restriction, index):
        return self.implement_coefficient(element, restriction, index, name_coefficientcontainer)

    def implement_trialfunction_gradient(self, element, restriction, index):
        derivative = self.indices[0]
        return self.implement_coefficient(element, restriction, index, name_coefficientcontainer, derivative=derivative)

    def implement_apply_function(self, element, restriction, index):
        return self.implement_coefficient(element, restriction, index, name_applycontainer)

    def implement_apply_function_gradient(self, element, restriction, index):
        derivative = self.indices[0]
        return self.implement_coefficient(element, restriction, index, name_applycontainer, derivative=derivative)

    def implement_coefficient(self, element, restriction, index, coeff_func, derivative=None):
        sub_element = element
        if isinstance(element, MixedElement):
            sub_element = element.extract_component(index)[1]
        from ufl import FiniteElement
        assert isinstance(sub_element, (FiniteElement, TensorProductElement))

        # Basis functions per direction
        basis_size = _basis_functions_per_direction(sub_element)

        # Construct the matrix sequence for this sum factorization
        matrix_sequence = construct_basis_matrix_sequence(derivative=derivative,
                                                          facedir=self.get_facedir(restriction),
                                                          facemod=self.get_facemod(restriction),
                                                          basis_size=basis_size)

        inp = LFSSumfactKernelInput(matrix_sequence=matrix_sequence,
                                    coeff_func=coeff_func,
                                    element=element,
                                    element_index=index,
                                    restriction=restriction,
                                    )

        position_priority = derivative
        if position_priority is None:
            position_priority = 3

        sf = SumfactKernel(matrix_sequence=matrix_sequence,
                           interface=inp,
                           position_priority=position_priority,
                           )

        from dune.codegen.sumfact.vectorization import attach_vectorization_info
        vsf = attach_vectorization_info(sf)

        self.indices = None

        # If this sum factorization kernel was not used in the dry run we
        # just return 0
        if vsf == 0:
            return 0

        # Add a sum factorization kernel that implements the evaluation of
        # the basis functions at quadrature points (stage 1)
        from dune.codegen.sumfact.realization import realize_sum_factorization_kernel
        var, _ = realize_sum_factorization_kernel(vsf)

        return prim.Subscript(var, vsf.quadrature_index(sf, self))


@basis_mixin("sumfact_pointdiagonal")
class SumfactPointDiagonalBasisMixin(SumfactBasisMixin):
    def lfs_inames(self, element, restriction, number=1):
        return ()

    def implement_basis(self, element, restriction, number):
        info = self.current_info[number]
        if element == info.element and restriction == info.restriction:
            return 1
        else:
            return 0

    def implement_reference_gradient(self, element, restriction, number):
        index, = self.indices
        self.indices = None
        info = self.current_info[number]
        if element == info.element and restriction == info.restriction and index == info.grad_index:
            return 1
        else:
            return 0


class LFSSumfactKernelInput(SumfactKernelInterfaceBase, ImmutableCuttingRecord):
    def __init__(self,
                 matrix_sequence=None,
                 coeff_func=None,
                 element=None,
                 element_index=0,
                 restriction=0,
                 ):

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
                                        coeff_func=coeff_func,
                                        element=element,
                                        element_index=element_index,
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
        return get_form_option("fastdg")

    def setup_input(self, sf, insn_dep, index=0):
        """Setup input for a sum factorization kernel function

        Write the coefficients into an array that can be passed to a sum
        factorization kernel function (necessary if direct input "fastdg" is
        not possible).

        index: Vectorization index
        """
        # Inames for interating over the coefficients. We take them from the
        # cost permuted matrix sequence. In order to get the inames in order
        # x,y,... we need to take the permutation back.
        shape_cost_permuted = tuple(mat.basis_size for mat in sf.matrix_sequence_cost_permuted)
        shape_ordered = permute_backward(shape_cost_permuted, self.cost_permutation)
        shape_ordered = permute_backward(shape_ordered, self.quadrature_permutation)
        inames_cost_permuted = tuple(sumfact_iname(length, "setup_inames_" + str(k)) for k, length in enumerate(shape_cost_permuted))
        inames_ordered = permute_backward(inames_cost_permuted, self.cost_permutation)
        inames_ordered = permute_backward(inames_ordered, self.quadrature_permutation)

        # The coefficient needs to be accessed with a flat index of inames ordered x,y,...
        flat_index = flatten_index(tuple(prim.Variable(i) for i in inames_ordered),
                                   shape_ordered,
                                   order="f")

        # Get the coefficient container
        lfs = name_lfs(self.element, self.restriction, self.element_index)
        container = self.coeff_func(self.restriction)
        from dune.codegen.pdelab.argument import pymbolic_coefficient as pc
        coeff = pc(container, lfs, flat_index)

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
        assignee = prim.Subscript(prim.Variable(name),
                                  (index,) + tuple(prim.Variable(i) for i in inames_cost_permuted))

        insn = instruction(assignee=assignee,
                           expression=coeff,
                           depends_on=sf.insn_dep.union(insn_dep),
                           tags=frozenset({"sumfact_stage{}".format(sf.stage)}),
                           )

        return insn_dep.union(frozenset({insn}))

    def realize_input(self, sf, inames, shape, vec_iname, vec_shape, buf, ftags):
        # Note: Here we do not need to reverse any permutation since this is
        # already done in the setup_input method above!

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

    def realize_direct_input(self, inames, shape, which=0):
        # If the input comes directly from a global data structure inames are
        # ordered x,y,z,...
        #
        # The inames and shape passed to this method come from the cost
        # permuted matrix sequence so we need to permute them back
        shape = permute_backward(shape, self.cost_permutation)
        shape = permute_backward(shape, self.quadrature_permutation)
        inames = permute_backward(inames, self.cost_permutation)
        inames = permute_backward(inames, self.quadrature_permutation)

        arg = "fastdg{}".format(which)

        from dune.codegen.sumfact.accumulation import _dof_offset
        globalarg(arg,
                  shape=shape,
                  dim_tags=",".join("f" * len(shape)),
                  offset=_dof_offset(self.element, self.element_index),
                  )

        return prim.Subscript(prim.Variable(arg), inames)

    @property
    def function_name_suffix(self):
        if get_form_option("fastdg"):
            return "_fastdg1_{}comp{}".format(FEM_name_mangling(self.element), self.element_index)
        else:
            return ""

    @property
    def function_args(self):
        if get_form_option("fastdg"):
            func = self.coeff_func(self.restriction)
            return ("{}.data()".format(func),)
        else:
            return ()

    @property
    def signature_args(self):
        if get_form_option("fastdg"):
            return ("const {}* fastdg0".format(type_floatingpoint()),)
        else:
            return ()

    @property
    def fastdg_interface_object_size(self):
        from dune.codegen.sumfact.accumulation import _local_sizes
        return sum(_local_sizes(self.element))


def _basis_functions_per_direction(element):
    """Number of basis functions per direction """
    from ufl import FiniteElement, TensorProductElement
    assert isinstance(element, (FiniteElement, TensorProductElement))
    degree = element.degree()
    if isinstance(degree, int):
        degree = (degree,) * world_dimension()

    basis_size = tuple(deg + 1 for deg in degree)

    # Anisotropic finite elements are not (yet) supported by Dune
    for size in basis_size:
        assert(size == basis_size[0])

    return basis_size


@iname
def sumfact_lfs_iname(element, bound, dim):
    assert(isinstance(bound, int))
    from dune.codegen.pdelab.driver import FEM_name_mangling
    name = "sumfac_lfs_{}_{}".format(FEM_name_mangling(element), dim)
    domain(name, bound)
    return name
