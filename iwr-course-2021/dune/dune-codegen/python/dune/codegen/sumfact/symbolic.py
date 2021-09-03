""" A pymbolic node representing a sum factorization kernel """

from dune.codegen.options import get_form_option, get_option
from dune.codegen.generation import (get_counted_variable,
                                     instruction,
                                     silenced_warning,
                                     subst_rule,
                                     transform,
                                     )
from dune.codegen.pdelab.geometry import local_dimension, world_dimension
from dune.codegen.sumfact.permutation import (flop_cost,
                                              permute_backward,
                                              permute_forward,
                                              sumfact_cost_permutation_strategy,
                                              sumfact_quadrature_permutation_strategy,
                                              )
from dune.codegen.sumfact.tabulation import BasisTabulationMatrixBase, BasisTabulationMatrixArray, quadrature_points_per_direction
from dune.codegen.loopy.target import dtype_floatingpoint, type_floatingpoint
from dune.codegen.loopy.vcl import ExplicitVCLCast, VCLLowerUpperLoad
from dune.codegen.tools import get_leaf, maybe_wrap_subscript, remove_duplicates

from pytools import ImmutableRecord, product

from ufl import MixedElement

import pymbolic.primitives as prim
import loopy as lp
import frozendict
import inspect


class SumfactKernelInterfaceBase(object):
    """A base class for the input/output of a sum factorization kernel
    In stage 1, this represents the input object, in stage 3 the output object.

    Notes about permutations:
    - setup_input: handle cost and quadrature permutation
    - realize_input stage 1: no permutations
    - realize_input stage 3: only cost permutation
    - realize_direct_input: cost and quadrature permutation
    - accumulate_output: no permutation
    - realize_direct_output: cost and quadrature permutation

    In the vectorized case most permutation handling is forwarded to the scalar
    kernels.
    """
    def setup_input(self, sf, insn_dep, index=0):
        """Create and fill an input array for a stage 1 sumfact kernel function (non fastdg)

        This happens before the function call. The input will be quadrature
        (for unstructured grids) and cost permuted.

        Parameters
        ----------
        sf : SumfactKernel or VectorizedSumfactKernel
        insn_dep : frozenset
            Instructions this setup depends on.
        index : int
            Vectorization index, SIMD lane.
        """
        raise NotImplementedError

    def realize_input(self, sf, inames, shape, vec_iname, vec_shape, buf, ftags):
        """Interpret the input of sumfact kernel function in the right way (non fastdgg)

        This happens inside the sumfact kernel function.

        Stage 1 : Input is already permuted the right way in setup_input.

        Stage 3 : The inames are cost and quadrature permuted but the input is
          only quadrature permuted. This means we need to reverse the cost
          permutation on the inames.

        Parameters
        ----------
        sf : SumfactKernel or VectorizedSumfactKernel
        inames : tuple of pymbolic.primitives.Variable
            Inames for accesing the input. Ordered according to permuted matrix sequence.
        shape : tuple of int
            Shape of input. Ordered according to permuted matrix sequence.
        vec_iname : tuple of pymbolic.primitives.Variable
            In case of vectorized kernel provide vectorization iname.
        vec_shape : tuple of int
            In case of vectorized kernel provide the number of vectorized kernels.
        buf : dune.codegen.sumfact.realization.BufferSwitcher
            Provides the input variable.
        ftags : str
            dim_tags needed to access input variable correctly.
        """
        raise NotImplementedError

    def realize_direct_input(self, inames, shape, which=0):
        """Interpret the input of sumfact kernel function in the right way (fastdg)

        This happens inside the sumfact kernel function.

        Stage 1: The input to the sum factorization kernel will be ordered x,
        y, z,... The shape and inames from this method come from the cost
        permuted matrix sequence. Make sure to permute them back when accesing
        the input.

        Parameters
        ----------
        inames : tuple of pymbolic.primitives.Variable
            Inames for accesing the input. Ordered according to permuted matrix sequence.
        shape: tuple of int
            Shape of input. Ordered according to permuted matrix sequence.
        which : int
            In case of VetcorizedSumfactKernel this might specify if the lower or upper
            part of a the SIMD register is for this input.
        """
        raise NotImplementedError

    def accumulate_output(self, sf, result, insn_dep, inames=None, additional_inames=()):
        """Generate accumulate instruction after a stage 3 sumfact kernel function (non fastdg)

        This happens after the function call. After stage 3 the result should
        be ordered x, y, z,..., no permutations necessary.

        Parameters
        ----------
        sf : SumfactKernel or VectorizedSumfactKernel
        result : SumfactKernel or some pymbolic stuff
            Result of a sum factorization
        insn_dep : frozenset
            Instructions this setup depends on.
        inames : tuple of pymbolic.primitives.Variable
        additional_inames : tuple of pymbolic.primitives.Variable
            Additional inames the accumulation instruction depends on (eg. loop over
            ansatz functions for jacobians).
        """
        raise NotImplementedError

    def realize_direct_output(self, result, iname, shape, which=0, **kwargs):
        """Accumulate results directly in the sumfact kernel function (fastdg)

        This happens inside the sumfact kernel function.

        Needs to handle cost and quadrature permutation.

        Parameters
        ----------
        result : pymbolic stuff
            Result of the sum factorization
        iname : tuple of pymbolic.primitives.Variable
        shape : tuple of ints
        which : int
            TODO Doc me!
        **kwargs :
            Key word arguments passed to loopy instruction
        """
        raise NotImplementedError

    @property
    def quadrature_permutation(self):
        """Order of local coordinate axis

        On unstructured grids we sometimes need to go through the directions in
        different order to make sure that we visit the (global) quadrature
        points on self and neighbor in the same order.
        """
        raise NotImplementedError

    @property
    def cost_permutation(self):
        """Permutation that minimizes flops
        """
        raise NotImplementedError

    @property
    def combined_permutation(self):
        return permute_forward(self.quadrature_permutation, self.cost_permutation)

    def permute_backward_cost(self, shape, inames):
        shape = permute_backward(shape, self.cost_permutation)
        inames = permute_backward(inames, self.cost_permutation)
        return shape, inames

    def permute_backward_quadrature(self, shape, inames):
        shape = permute_backward(shape, self.quadrature_permutation)
        inames = permute_backward(inames, self.quadrature_permutation)
        return shape, inames

    def permute_forward_cost(self, shape, inames):
        shape = permute_forward(shape, self.cost_permutation)
        inames = permute_forward(inames, self.cost_permutation)
        return shape, inames

    def permute_forward_quadrature(self, shape, inames):
        shape = permute_forward(shape, self.quadrature_permutation)
        inames = permute_forward(inames, self.quadrature_permutation)
        return shape, inames

    @property
    def within_inames(self):
        return ()

    @property
    def direct_is_possible(self):
        return False

    @property
    def stage(self):
        raise NotImplementedError

    @property
    def function_args(self):
        return ()

    @property
    def signature_args(self):
        return ()

    @property
    def function_name_suffix(self):
        return ""


class VectorSumfactKernelInput(SumfactKernelInterfaceBase):
    def __init__(self, interfaces):
        assert(isinstance(interfaces, tuple))
        self.interfaces = interfaces

    def __repr__(self):
        return "_".join(repr(i) for i in self.interfaces)

    @property
    def quadrature_permutation(self):
        # TODO: For now we only vectorize sumfact kernels with the same
        # quadrature permutation. This should be extended.
        for i in self.interfaces:
            assert i.quadrature_permutation == self.interfaces[0].quadrature_permutation
        return self.interfaces[0].quadrature_permutation

    @property
    def cost_permutation(self):
        # This should hold true due to the choice of quadrature
        # permutation. For both structured and unstructured grids the order of
        # the global directions should be the same leading to the same cost
        # permutation for all those sum factorization kernels.
        return self.interfaces[0].cost_permutation

    @property
    def stage(self):
        return 1

    @property
    def direct_is_possible(self):
        return all(i.direct_is_possible for i in self.interfaces)

    def setup_input(self, sf, dep):
        for i, inp in enumerate(self.interfaces):
            dep = dep.union(inp.setup_input(sf, dep, index=i))
        return dep

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

    def realize_direct_input(self, inames, shape):
        # Check whether the input exhibits a favorable structure
        # (whether we can broadcast scalar values into SIMD registers)
        total = set(self.interfaces)
        lower = set(self.interfaces[:len(self.interfaces) // 2])
        upper = set(self.interfaces[len(self.interfaces) // 2:])

        if len(total) == 1:
            # All input coefficients use the exact same input coefficient.
            # We implement this by broadcasting it into a SIMD register
            return prim.Call(ExplicitVCLCast(dtype_floatingpoint()),
                             (self.interfaces[0].realize_direct_input(inames, shape),)
                             )
        elif len(total) == 2 and len(lower) == 1 and len(upper) == 1:
            # The lower and the upper part of the SIMD register use
            # the same input coefficient, we combine the SIMD register
            # from two shorter SIMD types
            return prim.Call(VCLLowerUpperLoad(dtype_floatingpoint()),
                             (self.interfaces[0].realize_direct_input(inames, shape),
                              self.interfaces[len(self.interfaces) // 2].realize_direct_input(inames, shape, which=1),
                              )
                             )
        else:
            # The input does not exhibit a broadcastable structure, we
            # need to load scalars into the SIMD vector.
            raise NotImplementedError("SIMD loads from scalars not implemented!")

    @property
    def function_args(self):
        return sum((i.function_args for i in remove_duplicates(self.interfaces)), ())

    @property
    def signature_args(self):
        if self.interfaces[0].direct_is_possible:
            return tuple("const {}* fastdg{}".format(type_floatingpoint(), i) for i, _ in enumerate(remove_duplicates(self.interfaces)))
        else:
            return ()

    @property
    def function_name_suffix(self):
        return "".join(i.function_name_suffix for i in remove_duplicates(self.interfaces))

    @property
    def fastdg_interface_object_size(self):
        return self.interfaces[0].fastdg_interface_object_size


class VectorSumfactKernelOutput(SumfactKernelInterfaceBase):
    def __init__(self, interfaces):
        self.interfaces = interfaces

    def __repr__(self):
        return "_".join(repr(o) for o in self.interfaces)

    @property
    def cost_permutation(self):
        # This should hold true due to the choice of quadrature
        # permutation. For both structured and unstructured grids the order of
        # the global directions should be the same leading to the same cost
        # permutation for all those sum factorization kernels.
        for i in self.interfaces:
            assert i.cost_permutation == self.interfaces[0].cost_permutation
        return self.interfaces[0].cost_permutation

    @property
    def quadrature_permutation(self):
        # TODO: For now we only vectorize sumfact kernels with the same
        # quadrature permutation. This should be extended .
        for i in self.interfaces:
            assert i.quadrature_permutation == self.interfaces[0].quadrature_permutation
        return self.interfaces[0].quadrature_permutation

    @property
    def stage(self):
        return 3

    @property
    def within_inames(self):
        return self.interfaces[0].within_inames

    def _add_hadd(self, o, result):
        hadd_function = "horizontal_add"
        if len(set(self.interfaces)) > 1:
            pos = self.interfaces.index(o)
            if pos == 0:
                hadd_function = "horizontal_add_lower"
            else:
                hadd_function = "horizontal_add_upper"

        return prim.Call(prim.Variable(hadd_function), (result,))

    def realize_input(self, sf, inames, shape, vec_iname, vec_shape, buf, ftags):
        # The input for stage 3 is quadrature permuted. The inames and shape
        # passed to this method are quadrature and cost permuted. This means we
        # need to take the cost permutation back to get the right inames and
        # shape for interpreting the input!
        shape = permute_backward(shape, self.cost_permutation)
        inames = permute_backward(inames, self.cost_permutation)

        # Get a temporary that interprets the base storage of the input as a
        # column-major matrix.
        inp = buf.get_temporary(sf,
                                "buff_step0_in",
                                shape=shape + vec_shape,
                                dim_tags=ftags,
                                )

        # The input temporary will only be read from, so we need to silence
        # the loopy warning
        silenced_warning('read_no_write({})'.format(inp))

        return prim.Subscript(prim.Variable(inp), inames + vec_iname)

    def realize_direct_output(self, result, inames, shape, **args):
        outputs = set(self.interfaces)

        if len(outputs) > 1:
            # Introduce substrule for the argument of the horizontal add
            substname = "haddsubst_{}".format("_".join([i.name for i in inames]))
            subst_rule(substname, (), result)
            result = prim.Call(prim.Variable(substname), ())
            transform(lp.precompute, substname)

        deps = frozenset()
        for o in outputs:
            hadd_result = self._add_hadd(o, result)
            which = tuple(remove_duplicates(self.interfaces)).index(o)
            deps = deps.union(o.realize_direct_output(hadd_result,
                                                      inames,
                                                      shape,
                                                      which=which,
                                                      **args))

        return deps

    def accumulate_output(self, sf, result, insn_dep):
        outputs = set(self.interfaces)

        # Note: Using matrix_sequence_quadrature_permuted is ok in this place since:
        #
        # - If the grid is unstructured we assume that the polynomial degree
        #   for each direction is the same.
        #
        # - If the grid is structured the quadrature permuted matrix sequence
        #   is the same as the original one.  We still need to call this one
        #   since VectorizedSumfactKernels do not have the matrix_sequence
        #   attribute.
        basis_size = tuple(mat.basis_size for mat in sf.matrix_sequence_quadrature_permuted)
        if get_option('grid_unstructured'):
            assert len(set(basis_size)) == 1

        trial_element, = set(o.trial_element for o in self.interfaces)
        trial_element_index = set(o.trial_element_index for o in self.interfaces).pop()
        from dune.codegen.sumfact.accumulation import accum_iname
        element = get_leaf(trial_element, trial_element_index) if trial_element is not None else None
        inames = tuple(accum_iname(element, size, i) for i, size in enumerate(basis_size))
        veciname = accum_iname(element, sf.vector_width // len(outputs), "vec")
        transform(lp.tag_inames, [(veciname, "vec")])

        deps = frozenset()
        for o in outputs:
            hadd_result = self._add_hadd(o, maybe_wrap_subscript(result, tuple(prim.Variable(iname) for iname in inames + (veciname,))))
            deps = deps.union(o.accumulate_output(sf, hadd_result, insn_dep, inames=inames, additional_inames=(veciname,)))

        return deps

    @property
    def function_args(self):
        if get_form_option("fastdg"):
            return sum((i.function_args for i in remove_duplicates(self.interfaces)), ())
        else:
            return()

    @property
    def signature_args(self):
        if get_form_option("fastdg"):
            def _get_pair(i):
                ret = ("{}* fastdg{}".format(type_floatingpoint(), i),)
                if self.within_inames:
                    ret = ret + ("unsigned int jacobian_offset{}".format(i),)
                return ret
            return sum((_get_pair(i) for i, _ in enumerate(remove_duplicates(self.interfaces))), ())
        else:
            return ()

    @property
    def function_name_suffix(self):
        return "".join(i.function_name_suffix for i in remove_duplicates(self.interfaces))

    @property
    def fastdg_interface_object_size(self):
        return self.interfaces[0].fastdg_interface_object_size


class SumfactKernelBase(object):
    pass


class SumfactKernel(SumfactKernelBase, ImmutableRecord, prim.Variable):
    def __init__(self,
                 matrix_sequence=None,
                 buffer=None,
                 position_priority=None,
                 insn_dep=frozenset(),
                 interface=SumfactKernelInterfaceBase(),
                 predicates=frozenset(),
                 ):
        """Create a sum factorization kernel

        Sum factorization can be written as

        Y = R_{d-1} (A_{d-1} * ... * R_0 (A_0 * X)...)

        with:
        - X: Input rank d tensor of dimension n_0 x ... x n_{d-1}
        - Y: Output rank d tensor of dimension m_0 x ... x m_{d-1}
        - A_l: Values of 1D basis evaluations at quadrature points in l
               direction, matrix of dimension m_l x n_l
        - R_l: Transformation operator that permutes the underlying data
               vector of the rank d tensor in such a way that the fastest
               direction gets the slowest direction

        In the l'th step we have the following setup:
        - A_l: Matrix of dimensions m_l x n_l
        - X_l: Rank d tensor of dimensions n_l x ... x n_{d-1} x m_0 x ... x m_{l-1}
        - R_l: Transformation operator

        Looking at the indizes the following will happen:
        X --> [n_l,...,n_{d-1},m_0,...,m_{l-1}]
        A_l * X --> [m_l,n_l] * [n_l, ...] = [m_l,n_{l+1},...,n_{d-1},m_0,...,m_{l-1}]
        R_l (A_l*X) --> [n_{l+1},...,n_{d-1},m_0,...,m_{l-1}]

        So the multiplication with A_l is a reduction over one index and
        the transformation brings the next reduction index in the fastest
        position.

        In einsum notation from numpy this can be written as three contractions
        of the form: 'ij,jkl->kli'

        It can make sense to permute the order of directions. If you have
        a small m_l (e.g. stage 1 on faces) it is better to do direction l
        first. This can be done by:

        - Permuting the order of the A matrices.
        - Permuting the input tensor.
        - Permuting the output tensor (this assures that the directions of
          the output tensor are again ordered from 0 to d-1).

        Note, that you will typically *not* set all of the below arguments,
        but only some. The vectorization strategy may set others for you.
        The only argument really needed in all cases is matrix_sequence.

        Arguments:
        ----------
        matrix_sequence: A tuple of BasisTabulationMatrixBase instances The
            list of tensors to be applied to the input ordered from direction 0
            to d-1.  This might not be the order in which the tensors will be
            applied.
        buffer: A string identifying the flip flop buffer in use
            for intermediate results. The memory is expected to be
            pre-initialized with the input or you have to provide
            direct_input (FastDGGridOperator).
        position_priority: Will be used in the dry run to order kernels
            when doing vectorization e.g. (dx u,dy u,dz u, u).
        insn_dep: An instruction ID that the first issued instruction
            should depend upon. All following ones will depend on each
            other.
        interface: An SumfactKernelInterfaceBase instance describing the input
            (stage 1) or output (stage 3) of the kernel

        """
        # Assert the inputs!
        assert isinstance(matrix_sequence, tuple)
        assert all(isinstance(m, BasisTabulationMatrixBase) for m in matrix_sequence)
        assert isinstance(interface, SumfactKernelInterfaceBase)
        assert isinstance(insn_dep, frozenset)

        # The following construction is a bit weird: Dict comprehensions do not have
        # access to the locals of the calling scope: So we need to do the eval beforehand
        defaultdict = {}
        for a in SumfactKernel.init_arg_names:
            defaultdict[a] = eval(a)

        # Not sure if this whole permuting would make sense if we would do sum
        # factorized evaluation of intersections where len(matrix_sequence)
        # would not be equal to world dim.
        dim = len(matrix_sequence)
        assert dim == world_dimension()

        # Call the base class constructors
        ImmutableRecord.__init__(self, **defaultdict)
        prim.Variable.__init__(self, "SUMFACT")

        # Precompute and cache a number of keys
        self._cached_cache_key = None
        self._cached_flop_cost = {}

    #
    # The methods/fields needed to get a well-formed pymbolic node
    #

    def __getinitargs__(self):
        return tuple(getattr(self, arg) for arg in SumfactKernel.init_arg_names)

    def stringifier(self):
        # Uses __str__ below
        return lp.symbolic.StringifyMapper

    def __str__(self):
        # Return matrix_sequence_quadrature_permuted
        return "SF{}:[{}]->[{}]".format(self.stage,
                                        str(self.interface),
                                        ", ".join(str(m) for m in self.matrix_sequence_quadrature_permuted))

    mapper_method = "map_sumfact_kernel"

    #
    # Some cache key definitions
    # Watch out for the documentation to see which key is used unter what circumstances
    #
    @property
    def function_name(self):
        """ The name of the function that implements this kernel """
        # Use matrix_sequence_quadrature_permuted here since this is more consistent with
        # the vectorized case
        name = "sfimpl_{}{}".format("_".join(str(m) for m in self.matrix_sequence_quadrature_permuted),
                                    self.interface.function_name_suffix)

        # On unstructured we need different permutation of the input to realize
        # different permuation of quadrature points on self and neighbor. Mangle
        # the permutation of the quadrature points into the name to generate
        # sperate functions.
        if self.interface.quadrature_permutation != tuple(range(len(self.matrix_sequence))):
            name_quad_perm = "_qpperm_{}".format("".join(str(a) for a in self.interface.quadrature_permutation))
            name = name + name_quad_perm

        return name

    @property
    def parallel_key(self):
        """ A key that identifies parallellizable kernels. """
        # TODO: For now we do not vectorize SumfactKernels with different
        # quadrature_permutation. This should be handled like upper/lower
        # vectorization
        return tuple(m.basis_size for m in self.matrix_sequence_quadrature_permuted) + (self.stage, self.buffer, self.interface.within_inames) + (self.interface.direct_is_possible, self.interface.quadrature_permutation)

    @property
    def cache_key(self):
        """ The cache key that can be used in generation magic
        Any two sum factorization kernels having the same cache_key
        are realized simultaneously!
        """
        if self._cached_cache_key is None:
            if self.buffer is None:
                # During dry run, we return something unique to this kernel
                self._cached_cache_key = repr(self)
            else:
                # Later we identify parallely implemented kernels by the assigned buffer
                self._cached_cache_key = self.buffer

        return self._cached_cache_key

    @property
    def inout_key(self):
        """ A cache key for the input coefficients
        Any two sum factorization kernels having the same input_key
        work on the same input coefficient (stage 1) or accumulate
        into the same thing (stage 3)
        """
        return repr(self.interface)

    #
    # Some convenience methods to extract information about the sum factorization kernel
    #

    def __lt__(self, other):
        if self.parallel_key != other.parallel_key:
            return self.parallel_key < other.parallel_key
        if self.inout_key != other.inout_key:
            return self.inout_key < other.inout_key
        if self.position_priority == other.position_priority:
            return repr(self) < repr(other)
        if self.position_priority is None:
            return False
        if other.position_priority is None:
            return True
        return self.position_priority < other.position_priority

    @property
    def length(self):
        """ The number of matrices to apply """
        return len(self.matrix_sequence)

    @property
    def vectorized(self):
        return False

    @property
    def transposed(self):
        return self.matrix_sequence[0].transpose

    @property
    def within_inames(self):
        return self.interface.within_inames

    def vec_index(self, sf):
        """ Map an unvectorized sumfact kernel object to its position
        in the vectorized kernel
        """
        return 0

    @property
    def matrix_sequence_quadrature_permuted(self):
        """Matrix sequence ordered according to desired quadrature point ordered

        Except for face integrals on 3D unstructured grids this will just be
        the matrix sequence. In this special case it might be the reverse order
        to ensure that quadrature points are visited in the same order on self
        and neighbor.
        """
        perm = self.interface.quadrature_permutation
        matrix_sequence_quadrature_permuted = permute_forward(self.matrix_sequence, perm)
        return matrix_sequence_quadrature_permuted

    @property
    def matrix_sequence_cost_permuted(self):
        """Permute matrix_sequence_qudrature_permuted to minimize flop cost

        A clever ordering can lead to a reduced complexity. This will
        e.g. happen at faces where we only have one quadratue point m_l=1 if l
        is the normal direction of the face.

        Rule of thumb: small m's early and large n's late.
        """
        perm = sumfact_cost_permutation_strategy(self.matrix_sequence_quadrature_permuted, self.stage)
        matrix_sequence_cost_permuted = permute_forward(self.matrix_sequence_quadrature_permuted, perm)
        return matrix_sequence_cost_permuted

    @property
    def cost_permutation(self):
        return sumfact_cost_permutation_strategy(self.matrix_sequence_quadrature_permuted, self.stage)

    @property
    def quadrature_shape(self):
        """ The shape of a temporary for the quadrature points

        Takes into account the lower dimensionality of faces and vectorization.
        """
        return tuple(mat.quadrature_size for mat in self.matrix_sequence_quadrature_permuted)

    def quadrature_index(self, sf, visitor):
        quad_inames = visitor.quadrature_inames()
        if len(self.matrix_sequence_quadrature_permuted) == local_dimension():
            return tuple(prim.Variable(i) for i in quad_inames)

        # Traverse all the quadrature inames and map them to their correct direction
        index = []
        i = 0
        for d in range(world_dimension()):
            if self.matrix_sequence_quadrature_permuted[d].face is None:
                index.append(prim.Variable(quad_inames[i]))
                i = i + 1
            else:
                index.append(0)

        return tuple(index)

    @property
    def quadrature_dimtags(self):
        """ The dim_tags of a temporary for the quadrature points

        Takes into account the lower dimensionality of faces and vectorization.
        """
        tags = ["f"] * len(self.quadrature_shape)
        return ",".join(tags)

    @property
    def dof_shape(self):
        """ The shape of a temporary for the degrees of freedom

        Takes into account vectorization.
        """
        return tuple(mat.basis_size for mat in self.matrix_sequence_quadrature_permuted)

    @property
    def dof_dimtags(self):
        """ The dim_tags of a temporary for the degrees of freedom

        Takes into account vectorization.
        """
        tags = ["f"] * len(self.dof_shape)
        return ",".join(tags)

    @property
    def output_shape(self):
        if self.stage == 1:
            return self.quadrature_shape
        else:
            return self.dof_shape

    @property
    def output_dimtags(self):
        if self.stage == 1:
            return self.quadrature_dimtags
        else:
            return self.dof_dimtags

    @property
    def tag(self):
        return "sumfac"

    @property
    def stage(self):
        return self.interface.stage

    #
    # Define properties for conformity with the interface of VectorizedSumfactKernel
    #

    def padded_indices(self, visitor):
        return set()

    @property
    def horizontal_width(self):
        return 1

    def horizontal_index(self, _):
        return 0

    @property
    def vertical_width(self):
        return 1

    @property
    def vector_width(self):
        return 1

    #
    # Implement properties needed by cost models
    #

    @property
    def memory_traffic(self):
        """ The total number of bytes needed from RAM for the kernel
        to be executed - neglecting the existence of caches of course
        """
        input = product(mat.basis_size for mat in self.matrix_sequence)
        matrices = sum(mat.memory_traffic for mat in set(matrix_sequence))

        fbytes = get_option("precision_bits") / 8
        return (input + matrices) * fbytes

    @property
    def operations(self):
        """ The total number of floating point operations for the kernel
        to be carried out """
        qp = quadrature_points_per_direction()
        if qp not in self._cached_flop_cost:
            self._cached_flop_cost[qp] = flop_cost(self.matrix_sequence_cost_permuted)
        return self._cached_flop_cost[qp]


# Extract the argument list and store it on the class. This needs to be done
# outside of the class because the SumfactKernel class object needs to be fully
# initialized in order to extract the information from __init__.
SumfactKernel.init_arg_names = tuple(inspect.getargspec(SumfactKernel.__init__)[0][1:])


class VectorizedSumfactKernel(SumfactKernelBase, ImmutableRecord, prim.Variable):
    def __init__(self,
                 kernels=None,
                 horizontal_width=1,
                 vertical_width=1,
                 buffer=None,
                 insn_dep=frozenset(),
                 transformations=(),
                 ):
        # Assert the input data structure
        assert isinstance(kernels, tuple)
        assert all(isinstance(k, SumfactKernel) for k in kernels)

        # Assert all the properties that need to be the same across all subkernels
        assert len(set(k.stage for k in kernels)) == 1
        assert len(set(k.length for k in kernels)) == 1
        assert len(set(k.within_inames for k in kernels)) == 1
        assert len(set(k.predicates for k in kernels)) == 1

        # For now we don't mix direct and non_direct input. Could be done in an upper/lower way.
        assert len(set(tuple(k.interface.direct_is_possible for k in kernels))) == 1

        # Join the instruction dependencies of all subkernels
        insn_dep = insn_dep.union(k.insn_dep for k in kernels)

        # We currently assume that all subkernels are consecutive, 0-based within the vector
        assert None not in kernels

        ImmutableRecord.__init__(self,
                                 kernels=kernels,
                                 horizontal_width=horizontal_width,
                                 buffer=buffer,
                                 insn_dep=insn_dep,
                                 vertical_width=vertical_width,
                                 )

        prim.Variable.__init__(self, "VecSUMFAC")

        # Precompute and cache a number of keys
        self._cached_cache_key = None
        self._cached_flop_cost = {}

    def __getinitargs__(self):
        return (self.kernels, self.horizontal_width, self.vertical_width, self.buffer, self.insn_dep)

    def stringifier(self):
        return lp.symbolic.StringifyMapper

    def __str__(self):
        # Above stringifier just calls back into this
        return "VSF{}:[{}]->[{}]".format(self.stage,
                                         ", ".join(str(k.interface) for k in self.kernels),
                                         ", ".join(str(mat) for mat in self.matrix_sequence_quadrature_permuted))

    mapper_method = "map_vectorized_sumfact_kernel"

    init_arg_names = ("kernels", "horizontal_width", "vertical_width", "buffer", "insn_dep")

    #
    # Some cache key definitions
    # Watch out for the documentation to see which key is used unter what circumstances
    #
    @property
    def function_name(self):
        name = "sfimpl_{}{}".format("_".join(str(m) for m in self.matrix_sequence_quadrature_permuted),
                                    self.interface.function_name_suffix)
        return name

    @property
    def cache_key(self):
        """ The cache key that can be used in generation magic
        Any two sum factorization kernels having the same cache_key
        are realized simulatenously!
        """
        if self._cached_cache_key is None:
            self._cached_cache_key = (self.matrix_sequence_quadrature_permuted, self.restriction, self.stage, self.buffer)

        return self._cached_cache_key

    #
    # Deduce all data fields of normal sum factorization kernels from the underlying kernels
    #
    @property
    def matrix_sequence(self):
        # VectorizedSumfactKernel has no knowledge about the matrix_sequence
        # ordered according to directions 0,1,... since it is constructed based
        # on permuted matrix sequences.
        raise RuntimeError("matrix_sequence should not be used on VectorizedSumfactKernel.")

    @property
    def matrix_sequence_quadrature_permuted(self):
        # Construct quadrature permuted matrix sequence from scalar case
        return tuple(BasisTabulationMatrixArray(tuple(k.matrix_sequence_quadrature_permuted[i] for k in self.kernels),
                                                width=self.vector_width,
                                                )
                     for i in range(self.length))

    @property
    def matrix_sequence_cost_permuted(self):
        # Construct cost permuted matrix sequence from scalar case
        matrix_sequence = tuple(BasisTabulationMatrixArray(tuple(k.matrix_sequence_cost_permuted[i] for k in self.kernels),
                                                           width=self.vector_width,)
                                for i in range(self.length))

        # This should already be cost optimal
        perm = sumfact_cost_permutation_strategy(matrix_sequence, self.stage)
        assert perm == tuple(i for i in range(len(perm)))

        return matrix_sequence

    @property
    def cost_permutation(self):
        raise RuntimeError("cost_permutation should not be used on VectorizedSumfactKernel.")

    @property
    def stage(self):
        return self.kernels[0].stage

    @property
    def restriction(self):
        return self.kernels[0].restriction

    @property
    def quadrature_permutation(self):
        # The quadrature_permutations of the underlying scalar kernels can be
        # different from kernel to kernel. So there is no well defined
        # quadrature_permutation on the VectorizedSumfactKernel.
        raise RuntimeError("quadrature_permutation should not be used on VectorizedSumfactKernel.")

    @property
    def within_inames(self):
        return self.kernels[0].within_inames

    @property
    def predicates(self):
        return self.kernels[0].predicates

    @property
    def transposed(self):
        return self.kernels[0].transposed

    #
    # Define some properties only needed for this one
    #

    def padded_indices(self, visitor):
        indices = set(range(self.vector_width)) - set(range(len(self.kernels)))
        return tuple(self.kernels[0].quadrature_index(None, visitor) + (i,) for i in indices)

    @property
    def vector_width(self):
        return self.horizontal_width * self.vertical_width
    #
    # Define the same properties the normal SumfactKernel defines
    #

    @property
    def stage(self):
        return self.kernels[0].stage

    @property
    def interface(self):
        if self.stage == 1:
            return VectorSumfactKernelInput(tuple(k.interface for k in self.kernels))
        else:
            return VectorSumfactKernelOutput(tuple(k.interface for k in self.kernels))

    @property
    def cache_key(self):
        return (tuple(k.cache_key for k in self.kernels), self.buffer)

    @property
    def inout_key(self):
        return tuple(k.inout_key for k in self.kernels)

    @property
    def length(self):
        return self.kernels[0].length

    @property
    def vectorized(self):
        return True

    def horizontal_index(self, sf):
        for i, k in enumerate(self.kernels):
            if sf.interface == k.interface:
                if tuple(mat.derivative for mat in sf.matrix_sequence_quadrature_permuted) == tuple(mat.derivative for mat in k.matrix_sequence_quadrature_permuted):
                    return i

        return 0

    def _quadrature_index(self, sf, visitor):
        quad_inames = visitor.quadrature_inames()
        index = []

        if len(self.matrix_sequence_quadrature_permuted) == local_dimension():
            for d in range(local_dimension()):
                addindex = prim.Variable(quad_inames[d])

                if self.matrix_sequence_quadrature_permuted[d].slice_size:
                    addindex = addindex // self.vertical_width

                index.append(addindex)
        else:
            # Traverse all the quadrature inames and map them to their correct direction
            i = 0
            for d in range(world_dimension()):
                if self.matrix_sequence_quadrature_permuted[d].face is None:
                    addindex = prim.Variable(quad_inames[i])

                    if self.matrix_sequence_quadrature_permuted[d].slice_size:
                        addindex = addindex // self.vertical_width

                    index.append(addindex)
                    i = i + 1
                else:
                    index.append(0)

        return tuple(index)

    def vec_index(self, sf, visitor):
        quad_inames = visitor.quadrature_inames()

        sliced = 0
        if len(self.matrix_sequence_quadrature_permuted) == local_dimension():
            for d in range(local_dimension()):
                if self.matrix_sequence_quadrature_permuted[d].slice_size:
                    sliced = prim.Variable(quad_inames[d])
        else:
            i = 0
            for d in range(world_dimension()):
                if self.matrix_sequence_quadrature_permuted[d].face is None:
                    if self.matrix_sequence_quadrature_permuted[d].slice_size:
                        sliced = prim.Variable(quad_inames[i])
                    i = i + 1

        return self.horizontal_index(sf) + prim.Remainder(sliced, self.vertical_width)

    @property
    def quadrature_shape(self):
        return tuple(mat.quadrature_size for mat in self.matrix_sequence_quadrature_permuted) + (self.vector_width,)

    def quadrature_index(self, sf, visitor, direct_index=None):
        quad = self._quadrature_index(sf, visitor)
        if direct_index is not None:
            assert isinstance(direct_index, tuple)
            return quad + direct_index
        else:
            return quad + (self.vec_index(sf, visitor),)

    @property
    def quadrature_dimtags(self):
        tags = ["f"] * len(self.quadrature_shape)
        tags[-1] = 'c'
        return ",".join(tags)

    @property
    def dof_shape(self):
        return tuple(mat.basis_size for mat in self.matrix_sequence_quadrature_permuted) + (self.vector_width,)

    @property
    def dof_dimtags(self):
        tags = ["f"] * len(self.dof_shape)
        tags[-1] = 'vec'
        return ",".join(tags)

    @property
    def output_shape(self):
        if self.stage == 1:
            return self.quadrature_shape
        else:
            return self.dof_shape

    @property
    def output_dimtags(self):
        if self.stage == 1:
            return self.quadrature_dimtags
        else:
            return self.dof_dimtags

    @property
    def tag(self):
        return "vecsumfac_h{}_v{}".format(self.horizontal_width, self.vertical_width)

    #
    # Implement properties needed by cost models
    #

    @property
    def memory_traffic(self):
        """ The total number of bytes needed from RAM for the kernel
        to be executed - neglecting the existence of caches of course
        """
        dofs = product(mat.basis_size for mat in self.matrix_sequence_quadrature_permuted)
        matrices = sum(mat.memory_traffic for mat in set(self.matrix_sequence_quadrature_permuted))

        fbytes = get_option("precision_bits") / 8
        return (dofs + matrices) * fbytes

    @property
    def operations(self):
        """ The total number of floating point operations for the kernel
        to be carried out """
        qp = quadrature_points_per_direction()
        if qp not in self._cached_flop_cost:
            self._cached_flop_cost[qp] = flop_cost(self.matrix_sequence_cost_permuted)
        return self._cached_flop_cost[qp]
