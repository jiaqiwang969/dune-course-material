import itertools

from dune.codegen.pdelab.argument import (name_accumulation_variable,
                                          PDELabAccumulationFunction,
                                          )
from dune.codegen.generation import (accumulation_mixin,
                                     domain,
                                     dump_accumulate_timer,
                                     generator_factory,
                                     get_counted_variable,
                                     get_counter,
                                     get_global_context_value,
                                     globalarg,
                                     iname,
                                     instruction,
                                     post_include,
                                     kernel_cached,
                                     silenced_warning,
                                     temporary_variable,
                                     transform,
                                     valuearg
                                     )
from dune.codegen.options import (get_form_option,
                                  get_option,
                                  )
from dune.codegen.loopy.flatten import flatten_index
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.pdelab.driver import FEM_name_mangling
from dune.codegen.pdelab.localoperator import determine_accumulation_space, AccumulationMixinBase
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.pdelab.signatures import assembler_routine_name
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.pdelab.spaces import name_lfs
from dune.codegen.sumfact.permutation import (permute_backward,
                                              permute_forward,
                                              sumfact_cost_permutation_strategy,
                                              sumfact_quadrature_permutation_strategy,
                                              )
from dune.codegen.sumfact.tabulation import (basis_functions_per_direction,
                                             construct_basis_matrix_sequence,
                                             )
from dune.codegen.sumfact.symbolic import SumfactKernel, SumfactKernelInterfaceBase
from dune.codegen.ufl.modified_terminals import extract_modified_arguments
from dune.codegen.tools import get_pymbolic_basename, get_leaf, ImmutableCuttingRecord
from dune.codegen.error import CodegenError

from pytools import ImmutableRecord, product

import loopy as lp
import numpy as np
import pymbolic.primitives as prim
from loopy.symbolic import WalkMapper
import ufl.classes as uc
from ufl import FiniteElement, MixedElement, TensorProductElement
import itertools


basis_sf_kernels = generator_factory(item_tags=("basis_sf_kernels",), context_tags='kernel', no_deco=True)


class SumfactCollectMapper(WalkMapper):
    def map_sumfact_kernel(self, expr, *args, **kwargs):
        basis_sf_kernels(expr)
        self.visit(expr, *args, **kwargs)
        self.post_visit(expr, *args, **kwargs)


@iname
def _sumfact_iname(bound, _type, count):
    name = "sf_{}_{}".format(_type, str(count))
    domain(name, bound)
    return name


def sumfact_iname(bound, _type):
    count = get_counter('_sumfac_iname_{}'.format(_type))
    name = _sumfact_iname(bound, _type, count)
    return name


@kernel_cached
def accum_iname(element, bound, i):
    if element is None:
        suffix = ""
    else:
        from dune.codegen.pdelab.driver import FEM_name_mangling
        suffix = "_{}".format(FEM_name_mangling(element))
    return sumfact_iname(bound, "accum{}".format(suffix))


class AccumulationOutput(SumfactKernelInterfaceBase, ImmutableCuttingRecord):
    def __init__(self,
                 matrix_sequence=None,
                 accumvar=None,
                 restriction=None,
                 test_element=None,
                 test_element_index=None,
                 trial_element=None,
                 trial_element_index=None,
                 ):

        # See comment regarding get_keyword_arguments why we assert that matrix_sequence is not None
        assert matrix_sequence is not None

        # Note: The function sumfact_quadrature_permutation_strategy does not
        # work anymore after the visiting process since get_facedir and
        # get_facemod are not well defined. But we need the
        # quadrature_permutation to generate the name of the sumfact
        # kernel. This means we need to store the value here instead of
        # recalculating it in the property.
        dim = world_dimension()
        quadrature_permutation = sumfact_quadrature_permutation_strategy(dim, restriction[0])
        matrix_sequence = permute_forward(matrix_sequence, quadrature_permutation)

        # TODO: Isnt accumvar superfluous in the presence of all the other infos?
        # Note: Do not put matrix_sequence into the Record. That screws up the vectorization strategy!
        ImmutableCuttingRecord.__init__(self,
                                        accumvar=accumvar,
                                        restriction=restriction,
                                        test_element=test_element,
                                        test_element_index=test_element_index,
                                        trial_element=trial_element,
                                        trial_element_index=trial_element_index,
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
        return 3

    @property
    def direct_is_possible(self):
        return get_form_option("fastdg")

    @property
    def within_inames(self):
        if self.trial_element is None:
            return ()
        else:
            mixin = get_form_option("basis_mixins")
            from dune.codegen.generation import construct_from_mixins
            MixinType = construct_from_mixins(mixins=[mixin], mixintype="basis", name="MixinType")
            return MixinType.lfs_inames(MixinType(), get_leaf(self.trial_element, self.trial_element_index), self.restriction)

    def realize_input(self, sf, inames, shape, vec_iname, vec_shape, buf, ftags):
        # The result of stage 2 has the correct quadrature permutation but no
        # cost permutation is applied. The inames for this method are
        # quadrature and cost permuted. This means we need to reverse the cost
        # permutation to access the result of stage 2 in the correct way.
        shape = permute_backward(shape, self.cost_permutation)
        inames = permute_backward(inames, self.cost_permutation)

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

    def accumulate_output(self, sf, result, insn_dep, inames=None, additional_inames=()):
        trial_leaf_element = get_leaf(self.trial_element, self.trial_element_index) if self.trial_element is not None else None

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

        if inames is None:
            inames = tuple(accum_iname(trial_leaf_element, size, i) for i, size in enumerate(basis_size))

            # Determine the expression to accumulate with. This depends on the vectorization strategy!
            from dune.codegen.tools import maybe_wrap_subscript
            result = maybe_wrap_subscript(result, tuple(prim.Variable(i) for i in inames))

        # Collect the lfs and lfs indices for the accumulate call
        restriction = (0, 0) if self.restriction is None else self.restriction
        test_lfs = name_lfs(self.test_element, restriction[0], self.test_element_index)
        valuearg(test_lfs, dtype=lp.types.NumpyType("str"))
        test_lfs_index = flatten_index(tuple(prim.Variable(i) for i in inames),
                                       basis_size,
                                       order="f"
                                       )

        accum_args = [prim.Variable(test_lfs), test_lfs_index]

        # In the jacobian case, also determine the space for the ansatz space
        if sf.within_inames:
            # TODO the next line should get its inames from
            # elsewhere. This is *NOT* robust (but works right now)
            ansatz_lfs = name_lfs(self.trial_element, restriction[1], self.trial_element_index)
            valuearg(ansatz_lfs, dtype=lp.types.NumpyType("str"))
            from dune.codegen.sumfact.basis import _basis_functions_per_direction
            ansatz_lfs_index = flatten_index(tuple(prim.Variable(sf.within_inames[i])
                                                   for i in range(world_dimension())),
                                             _basis_functions_per_direction(trial_leaf_element),
                                             order="f"
                                             )

            accum_args.append(prim.Variable(ansatz_lfs))
            accum_args.append(ansatz_lfs_index)

        accum_args.append(result)

        if not get_form_option("fastdg"):
            rank = 2 if self.within_inames else 1
            expr = prim.Call(PDELabAccumulationFunction(self.accumvar, rank),
                             tuple(accum_args)
                             )
            dep = instruction(assignees=(),
                              expression=expr,
                              forced_iname_deps=frozenset(inames + additional_inames + self.within_inames),
                              forced_iname_deps_is_final=True,
                              depends_on=insn_dep,
                              predicates=sf.predicates,
                              tags=frozenset({"sumfact_stage3"}),
                              )

        return frozenset({dep})

    def realize_direct_output(self, result, inames, shape, which=0, **args):
        inames = permute_backward(inames, self.cost_permutation)
        inames = permute_backward(inames, self.quadrature_permutation)

        direct_output = "fastdg{}".format(which)
        ftags = ",".join(["f"] * len(shape))

        if self.trial_element is None:
            globalarg(direct_output,
                      shape=shape,
                      dim_tags=ftags,
                      offset=_dof_offset(self.test_element, self.test_element_index),
                      )
            lhs = prim.Subscript(prim.Variable(direct_output), inames)
        else:
            rowsize = sum(tuple(s for s in _local_sizes(self.trial_element)))
            manual_strides = tuple("stride:{}".format(rowsize * product(shape[:i])) for i in range(len(shape)))
            offset = "jacobian_offset{}".format(which)
            valuearg(offset)
            globalarg(direct_output,
                      shape=shape,
                      offset=prim.Variable(offset) + rowsize * _dof_offset(self.test_element, self.test_element_index) + _dof_offset(self.trial_element, self.trial_element_index),
                      dim_tags=manual_strides,
                      )
            lhs = prim.Subscript(prim.Variable(direct_output), inames)

        result = prim.Sum((lhs, result))
        return frozenset({instruction(assignee=lhs,
                                      expression=result,
                                      tags=frozenset({"sumfact_stage3"}),
                                      **args)})

    @property
    def function_name_suffix(self):
        if get_form_option("fastdg"):
            suffix = "_fastdg1_{}comp{}".format(FEM_name_mangling(self.test_element), self.test_element_index)
            if self.within_inames:
                suffix = "{}x{}comp{}".format(suffix, FEM_name_mangling(self.trial_element), self.trial_element_index)
            return suffix
        else:
            return ""

    @property
    def function_args(self):
        if get_form_option("fastdg"):
            ret = ("{}.data()".format(self.accumvar),)
            if get_form_option("fastdg") and self.within_inames:
                element = get_leaf(self.trial_element, self.trial_element_index)
                shape = tuple(element.degree() + 1 for e in range(element.cell().geometric_dimension()))
                jacobian_index = flatten_index(tuple(prim.Variable(i) for i in self.within_inames), shape, order="f")
                ret = ret + (str(jacobian_index),)
            return ret
        else:
            return ()

    @property
    def signature_args(self):
        if get_form_option('fastdg'):
            ret = ("{}* fastdg0".format(type_floatingpoint()),)
            if self.within_inames:
                ret = ret + ("unsigned int jacobian_offset0",)
            return ret
        else:
            return ()

    @property
    def fastdg_interface_object_size(self):
        size = sum(_local_sizes(self.trial_element)) if self.trial_element else 1
        return size * sum(_local_sizes(self.test_element))


def _local_sizes(element):
    from ufl import FiniteElement, MixedElement
    if isinstance(element, MixedElement):
        for subel in element.sub_elements():
            for s in _local_sizes(subel):
                yield s
    else:
        assert isinstance(element, FiniteElement)
        yield (element.degree() + 1)**element.cell().geometric_dimension()


def _dof_offset(element, component):
    if component is None:
        return 0
    else:
        sizes = tuple(s for s in _local_sizes(element))
        return sum(sizes[0:component])


@accumulation_mixin("sumfact")
class SumfactAccumulationMixin(AccumulationMixinBase):
    def get_accumulation_info(self, expr):
        return get_accumulation_info(expr, self)

    def list_accumulation_infos(self, expr):
        return itertools.product(_gradsplitting_generator(expr, self),
                                 _trial_generator(expr, self),
                                 )

    def generate_accumulation_instruction(self, expr):
        return generate_accumulation_instruction(expr, self)

    def get_facedir(self, restriction):
        from dune.codegen.pdelab.restriction import Restriction
        if restriction == Restriction.POSITIVE or get_global_context_value("integral_type") == "exterior_facet":
            return get_global_context_value("facedir_s")
        if restriction == Restriction.NEGATIVE:
            return get_global_context_value("facedir_n")
        return None

    def get_facemod(self, restriction):
        from dune.codegen.pdelab.restriction import Restriction
        if restriction == Restriction.POSITIVE or get_global_context_value("integral_type") == "exterior_facet":
            return get_global_context_value("facemod_s")
        if restriction == Restriction.NEGATIVE:
            return get_global_context_value("facemod_n")
        return None

    def additional_matrix_sequence(self):
        return None

    @property
    def prohibit_jacobian(self):
        return False


@accumulation_mixin("sumfact_pointdiagonal")
class SumfactPointDiagonalAccumulationMixin(SumfactAccumulationMixin):
    def additional_matrix_sequence(self):
        info = self.current_info[1]
        return construct_basis_matrix_sequence(transpose=True,
                                               derivative=info.grad_index,
                                               facedir=self.get_facedir(info.restriction),
                                               facemod=self.get_facemod(info.restriction),
                                               basis_size=get_basis_size(info),
                                               )

    def get_accumulation_info(self, expr):
        element = expr.ufl_element()
        leaf_element = element
        element_index = 0
        from ufl import MixedElement
        if isinstance(expr.ufl_element(), MixedElement):
            element_index = self.indices[0]
            leaf_element = element.extract_component(element_index)[1]

        restriction = self.restriction
        if self.measure == 'exterior_facet':
            from dune.codegen.pdelab.restriction import Restriction
            restriction = Restriction.POSITIVE

        grad_index = None
        if self.reference_grad:
            if isinstance(expr.ufl_element(), MixedElement):
                grad_index = self.indices[1]
            else:
                grad_index = self.indices[0]

        return SumfactAccumulationInfo(element=expr.ufl_element(),
                                       element_index=element_index,
                                       restriction=restriction,
                                       grad_index=grad_index,
                                       )

    def list_accumulation_infos(self, expr):
        return itertools.product(_gradsplitting_generator(expr, self, number=0),
                                 _gradsplitting_generator(expr, self, number=1),
                                 )

    @property
    def prohibit_jacobian(self):
        return True


class SumfactAccumulationInfo(ImmutableRecord):
    def __init__(self,
                 element=None,
                 element_index=0,
                 restriction=None,
                 inames=(),
                 grad_index=None,
                 ):
        ImmutableRecord.__init__(self,
                                 element=element,
                                 element_index=element_index,
                                 restriction=restriction,
                                 inames=inames,
                                 grad_index=grad_index,
                                 )

    def __eq__(self, other):
        return type(self) == type(other) and self.element_index == other.element_index and self.restriction == other.restriction and self.grad_index == other.grad_index

    def __hash__(self):
        return (self.element_index, self.restriction, self.grad_index)


def get_accumulation_info(expr, visitor):
    element = expr.ufl_element()
    leaf_element = element
    element_index = 0
    from ufl import MixedElement
    if isinstance(expr.ufl_element(), MixedElement):
        element_index = visitor.indices[0]
        leaf_element = element.extract_component(element_index)[1]

    restriction = visitor.restriction
    if visitor.measure == 'exterior_facet':
        from dune.codegen.pdelab.restriction import Restriction
        restriction = Restriction.POSITIVE

    inames = visitor.lfs_inames(leaf_element,
                                restriction,
                                expr.number()
                                )

    grad_index = None
    if visitor.reference_grad and expr.number() == 0:
        if isinstance(expr.ufl_element(), MixedElement):
            grad_index = visitor.indices[1]
        else:
            grad_index = visitor.indices[0]

    return SumfactAccumulationInfo(element=expr.ufl_element(),
                                   element_index=element_index,
                                   restriction=restriction,
                                   inames=inames,
                                   grad_index=grad_index,
                                   )


def _get_childs(element):
    if isinstance(element, (FiniteElement, TensorProductElement)):
        yield (0, element)
    else:
        for i in range(element.value_size()):
            yield (i, element.extract_component(i)[1])


def _gradsplitting_generator(expr, visitor, number=0):
    from dune.codegen.ufl.modified_terminals import extract_modified_arguments
    ma = extract_modified_arguments(expr, argnumber=number)
    if len(ma) == 0:
        return
    element = ma[0].argexpr.ufl_element()
    dim = world_dimension()

    from dune.codegen.ufl.modified_terminals import Restriction
    if visitor.measure == "cell":
        restrictions = (Restriction.NONE,)
    elif visitor.measure == "exterior_facet":
        restrictions = (Restriction.POSITIVE,)
    elif visitor.measure == "interior_facet":
        restrictions = (Restriction.POSITIVE, Restriction.NEGATIVE)
    for res in restrictions:
        for ei, e in _get_childs(element):
            for grad in (None,) + tuple(range(dim)):
                yield SumfactAccumulationInfo(element=element,
                                              element_index=ei,
                                              restriction=res,
                                              grad_index=grad)


def _trial_generator(expr, visitor):
    from dune.codegen.ufl.modified_terminals import extract_modified_arguments
    ma = extract_modified_arguments(expr, argnumber=1)
    if len(ma) == 0:
        yield None
        return
    element = ma[0].argexpr.ufl_element()

    from dune.codegen.ufl.modified_terminals import Restriction
    if visitor.measure == "cell":
        restrictions = (Restriction.NONE,)
    elif visitor.measure == "exterior_facet":
        restrictions = (Restriction.POSITIVE,)
    elif visitor.measure == "interior_facet":
        restrictions = (Restriction.POSITIVE, Restriction.NEGATIVE)
    for res in restrictions:
        for ei, e in _get_childs(element):
            yield SumfactAccumulationInfo(element_index=ei, restriction=res, element=e)


def get_basis_size(info):
    leaf_element = info.element
    element_index = info.element_index
    dim = world_dimension()
    from ufl import MixedElement
    if isinstance(leaf_element, MixedElement):
        leaf_element = leaf_element.extract_component(element_index)[1]
    degree = leaf_element._degree
    if isinstance(degree, int):
        degree = (degree,) * dim
    return tuple(deg + 1 for deg in degree)


def generate_accumulation_instruction(expr, visitor):
    test_info = visitor.test_info
    trial_info = visitor.trial_info

    # Count flops on the expression for the vectorization decision making algorithm
    from dune.codegen.sumfact.vectorization import count_quadrature_point_operations
    count_quadrature_point_operations(expr)

    # Number of basis functions per direction
    basis_size = get_basis_size(test_info)

    # Anisotropic finite elements are not (yet) supported by Dune
    assert(size == basis_size[0] for size in basis_size)

    from dune.codegen.pdelab.localoperator import boundary_predicates
    predicates = boundary_predicates(visitor.measure,
                                     visitor.subdomain_id,
                                     )
    if False in predicates:
        return

    # Cache all stage 1 sum factorization kernels used in this expression
    SumfactCollectMapper()(expr)

    insn_dep = None

    from dune.codegen.pdelab.localoperator import determine_accumulation_space
    test_lfs = determine_accumulation_space(test_info, 0)
    ansatz_lfs = determine_accumulation_space(trial_info, 1)

    if trial_info is None:
        trial_info = SumfactAccumulationInfo()
    trial_leaf_element = trial_info.element
    from ufl import MixedElement
    if isinstance(trial_leaf_element, MixedElement):
        trial_leaf_element = trial_leaf_element.extract_component(trial_info.element_index)[1]

    from dune.codegen.pdelab.argument import name_accumulation_variable
    accumvar = name_accumulation_variable(test_lfs.get_restriction() + ansatz_lfs.get_restriction())

    matrix_sequence = construct_basis_matrix_sequence(
        transpose=True,
        derivative=test_info.grad_index,
        facedir=visitor.get_facedir(test_info.restriction),
        facemod=visitor.get_facemod(test_info.restriction),
        basis_size=basis_size,
        additional_sequence=visitor.additional_matrix_sequence())

    jacobian_inames = trial_info.inames
    priority = test_info.grad_index
    if priority is None:
        priority = 3

    trial_element = trial_info.element
    trial_element_index = trial_info.element_index
    if visitor.prohibit_jacobian:
        trial_element = None
        trial_element_index = 0

    output = AccumulationOutput(matrix_sequence=matrix_sequence,
                                accumvar=accumvar,
                                restriction=(test_info.restriction, trial_info.restriction),
                                test_element=test_info.element,
                                test_element_index=test_info.element_index,
                                trial_element=trial_element,
                                trial_element_index=trial_element_index,
                                )

    sf = SumfactKernel(matrix_sequence=matrix_sequence,
                       position_priority=priority,
                       interface=output,
                       predicates=predicates,
                       )

    from dune.codegen.sumfact.vectorization import attach_vectorization_info
    vsf = attach_vectorization_info(sf)

    # Make sure we have a buffer that we can set up the input with
    buffer = vsf.buffer
    if buffer is None:
        buffer = get_counted_variable("buffer")

    vectag = frozenset({"gradvec"}) if vsf.vectorized else frozenset()

    from dune.codegen.sumfact.realization import name_buffer_storage
    temp = "input_{}".format(buffer)
    temporary_variable(temp,
                       shape=vsf.quadrature_shape,
                       dim_tags=vsf.quadrature_dimtags,
                       custom_base_storage=name_buffer_storage(buffer, 0),
                       managed=True,
                       )

    # Those input fields, that are padded need to be set to zero
    # in order to do a horizontal_add later on
    for pad in vsf.padded_indices(visitor):
        assignee = prim.Subscript(lp.TaggedVariable(temp, vsf.tag), pad)
        instruction(assignee=assignee,
                    expression=0,
                    forced_iname_deps=frozenset(visitor.quadrature_inames() + jacobian_inames),
                    forced_iname_deps_is_final=True,
                    tags=frozenset(["quadvec", "gradvec"]),
                    )

    # Determine dependencies
    from loopy.match import Or, Writes
    from loopy.symbolic import DependencyMapper
    from dune.codegen.tools import get_pymbolic_basename
    deps = Or(tuple(Writes(get_pymbolic_basename(e)) for e in DependencyMapper()(expr)))

    # Issue an instruction in the quadrature loop that fills the buffer
    # with the evaluation of the contribution at all quadrature points
    assignee = prim.Subscript(lp.TaggedVariable(temp, vsf.tag),
                              vsf.quadrature_index(sf, visitor))

    contrib_dep = instruction(assignee=assignee,
                              expression=expr,
                              forced_iname_deps=frozenset(visitor.quadrature_inames() + jacobian_inames),
                              forced_iname_deps_is_final=True,
                              tags=frozenset({"quadvec", "sumfact_stage2"}).union(vectag),
                              depends_on=frozenset({deps}).union(frozenset({lp.match.Tagged("sumfact_stage1")})),
                              no_sync_with=frozenset({(lp.match.Tagged("sumfact_stage2"), "any")}),
                              )

    if insn_dep is None:
        insn_dep = frozenset({contrib_dep})

    # Add a sum factorization kernel that implements the multiplication
    # with the test function (stage 3)
    from dune.codegen.sumfact.realization import realize_sum_factorization_kernel
    result, insn_dep = realize_sum_factorization_kernel(vsf.copy(insn_dep=vsf.insn_dep.union(insn_dep)))

    if not get_form_option("fastdg"):
        insn_dep = vsf.interface.accumulate_output(vsf, result, insn_dep)
