"""
The code that triggers the creation of the necessary code constructs
to realize a sum factorization kernel
"""
from dune.codegen.generation import (barrier,
                                     delete_cache_items,
                                     dump_accumulate_timer,
                                     generator_factory,
                                     get_global_context_value,
                                     globalarg,
                                     instruction,
                                     kernel_cached,
                                     post_include,
                                     preamble,
                                     silenced_warning,
                                     temporary_variable,
                                     transform,
                                     )
from dune.codegen.loopy.flatten import flatten_index
from dune.codegen.pdelab.basis import shape_as_pymbolic
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.options import (get_form_option,
                                  get_option,
                                  )
from dune.codegen.pdelab.signatures import assembler_routine_name
from dune.codegen.sumfact.permutation import (permute_backward,
                                              permute_forward,
                                              )
from dune.codegen.sumfact.quadrature import quadrature_points_per_direction
from dune.codegen.sumfact.symbolic import (SumfactKernel,
                                           VectorizedSumfactKernel,
                                           )
from dune.codegen.sumfact.accumulation import sumfact_iname
from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.loopy.vcl import ExplicitVCLCast
from dune.codegen.tools import get_leaf, remove_duplicates

from pytools import product
from ufl import MixedElement

import loopy as lp
import numpy as np
import pymbolic.primitives as prim


# Have a generator function store the necessary sum factorization kernel implementations
# This way then can easily be extracted at the end of the form visiting process
necessary_kernel_implementations = generator_factory(item_tags=("kernelimpl",), cache_key_generator=lambda a: a[0].function_name, no_deco=True)


def realize_sum_factorization_kernel(sf, **kwargs):
    if get_global_context_value("dry_run", False):
        return sf, sf.insn_dep
    else:
        return _realize_sum_factorization_kernel(sf, **kwargs)


def name_buffer_storage(buff, which):
    name = "{}_{}".format(buff, which)
    return name


def _max_sum_factorization_buffer_size(sf):
    size = max(product(m.quadrature_size for m in sf.matrix_sequence_cost_permuted) * sf.vector_width,
               product(m.basis_size for m in sf.matrix_sequence_cost_permuted) * sf.vector_width)
    return size


@kernel_cached
def _realize_sum_factorization_kernel(sf):
    insn_dep = sf.insn_dep

    # Get all the necessary pieces for a function call
    buffers = tuple(name_buffer_storage(sf.buffer, i) for i in range(2))

    # Make sure that the storage is allocated and has a certain minimum size
    # This is necessary to allocate buffers that will be passed to sumfact kernel
    # functions. Loopy has no knowledge of what happens with those...
    for buf in buffers:
        # Determine the necessary size of the buffer. We assume that we do not
        # underintegrate the form!!!
        size = _max_sum_factorization_buffer_size(sf)
        temporary_variable("{}_dummy".format(buf),
                           shape=(size,),
                           custom_base_storage=buf,
                           decl_method=lambda n, k, di: None,
                           )

    # Realize the input if it is not direct
    if sf.stage == 1 and not sf.interface.direct_is_possible:
        insn_dep = insn_dep.union(sf.interface.setup_input(sf, insn_dep))

    # Trigger generation of the sum factorization kernel function
    qp = quadrature_points_per_direction()
    necessary_kernel_implementations((sf, qp))

    # Call the function
    code = "{}({});".format(sf.function_name, ", ".join(buffers + sf.interface.function_args))
    tag = "sumfact_stage{}".format(sf.stage)
    insn_dep = frozenset({instruction(code=code,
                                      depends_on=insn_dep,
                                      within_inames=frozenset(sf.within_inames),
                                      tags=frozenset({tag}),
                                      predicates=sf.predicates,
                                      )
                          })

    # Interpret the output as a temporary of correct shape
    out = "{}_output".format(sf.buffer)
    temporary_variable(out,
                       shape=sf.output_shape,
                       dim_tags=sf.output_dimtags,
                       custom_base_storage=buffers[sf.length % 2],
                       managed=True,
                       )
    silenced_warning("read_no_write({})".format(out))

    return lp.TaggedVariable(out, sf.tag), insn_dep


class BufferSwitcher(object):
    def __init__(self):
        self.current = 0

    def get_temporary(self, sf=None, name=None, **kwargs):
        assert sf
        assert name

        bs = "buffer{}".format(self.current)
        shape = kwargs['shape']
        assert shape
        dim_tags = kwargs['dim_tags'].split(',')
        assert dim_tags

        # Calculate correct alignment
        vec_size = 1
        if 'vec' in dim_tags:
            vec_size = shape[dim_tags.index('vec')]
        from dune.codegen.loopy.target import dtype_floatingpoint
        dtype = np.dtype(kwargs.get("dtype", dtype_floatingpoint()))
        alignment = dtype.itemsize * vec_size

        # Add this buffer as global argument to the kernel. Add a shape to make
        # benchmark generation for autotuning of loopy kernels easier. Since
        # this buffer is used to store different data sizes we need to make
        # sure it is big enough.
        assert sf
        size = _max_sum_factorization_buffer_size(sf)
        globalarg(bs, shape=(size,), alignment=alignment, dim_tags=['f', ])

        temporary_variable(name,
                           managed=True,
                           custom_base_storage=bs,
                           **kwargs
                           )

        return name

    def switch(self):
        self.current = (self.current + 1) % 2


def realize_sumfact_kernel_function(sf):
    # Remove anything kernel related from caches
    delete_cache_items("kernel_default")

    # Get a buffer switcher instance
    buffer = BufferSwitcher()
    insn_dep = frozenset()

    # Prepare some dim_tags/shapes for later use
    ftags = ",".join(["f"] * sf.length)
    novec_ftags = ftags
    ctags = ",".join(["c"] * sf.length)
    vec_shape = ()
    if sf.vectorized:
        ftags = ftags + ",vec"
        ctags = ctags + ",vec"
        vec_shape = (sf.vector_width,)

    # Matrix sequence of this sum factorization kernel
    matrix_sequence = sf.matrix_sequence_cost_permuted

    # Product of all matrices
    for l, matrix in enumerate(matrix_sequence):
        # Compute the correct shapes of in- and output matrices of this matrix-matrix multiplication
        # and get inames that realize the product.
        inp_shape = (matrix.cols,) \
            + tuple(mat.cols for mat in matrix_sequence[l + 1:]) \
            + tuple(mat.rows for mat in matrix_sequence[:l])
        out_shape = (matrix.rows,) \
            + tuple(mat.cols for mat in matrix_sequence[l + 1:]) \
            + tuple(mat.rows for mat in matrix_sequence[:l])
        out_inames = tuple(sumfact_iname(length, "out_inames_" + str(k)) for k, length in enumerate(out_shape))
        vec_iname = ()
        if matrix.vectorized:
            iname = sumfact_iname(sf.vector_width, "vec")
            vec_iname = (prim.Variable(iname),)
            transform(lp.tag_inames, [(iname, "vec")])

        # A trivial reduction is implemented as a product, otherwise we run into
        # a code generation corner case producing way too complicated code. This
        # could be fixed upstream, but the loopy code realizing reductions is not
        # trivial and the priority is kind of low.
        if matrix.cols == 1:
            k_expr = 0
        else:
            k = sumfact_iname(matrix.cols, "red")
            k_expr = prim.Variable(k)

        # Setup the input of the sum factorization kernel. In the
        # first matrix multiplication this can be taken from
        # * an input temporary (default)
        # * a global data structure (if FastDGGridOperator is in use)
        # * a value from a global data structure, broadcasted to a vector type
        #   (vectorized + FastDGGridOperator)
        input_inames = (k_expr,) + tuple(prim.Variable(j) for j in out_inames[1:])

        if l == 0 and sf.stage == 1 and sf.interface.direct_is_possible:
            input_summand = sf.interface.realize_direct_input(input_inames, inp_shape)
        elif l == 0:
            input_summand = sf.interface.realize_input(sf,
                                                       input_inames,
                                                       inp_shape,
                                                       vec_iname,
                                                       vec_shape,
                                                       buffer,
                                                       ftags,
                                                       )
        else:
            # Get a temporary that interprets the base storage of the input
            # as a column-major matrix. In later iteration of the matrix loop
            # this reinterprets the output of the previous iteration.
            inp = buffer.get_temporary(sf,
                                       "buff_step{}_in".format(l),
                                       shape=inp_shape + vec_shape,
                                       dim_tags=ftags,
                                       )

            # The input temporary will only be read from, so we need to silence
            # the loopy warning
            silenced_warning('read_no_write({})'.format(inp))

            input_summand = prim.Subscript(prim.Variable(inp),
                                           input_inames + vec_iname)

        buffer.switch()

        # Write the matrix-matrix multiplication expression
        matprod = prim.Product((matrix.pymbolic((prim.Variable(out_inames[0]), k_expr) + vec_iname),
                                input_summand))

        # ... which may be a reduction, if k>0
        if matrix.cols != 1:
            matprod = lp.Reduction("sum", k, matprod)

        # Here we also move the new direction (out_inames[0]) to the end
        output_inames = tuple(prim.Variable(i) for i in out_inames[1:]) + (prim.Variable(out_inames[0]),)

        # Collect the key word arguments for the loopy instruction
        insn_args = {"depends_on": insn_dep}

        # In case of direct output we directly accumulate the result
        # of the Sumfactorization into some global data structure.
        if l == len(matrix_sequence) - 1 and get_form_option('fastdg') and sf.stage == 3:
            if sf.vectorized:
                insn_args["forced_iname_deps"] = frozenset({vec_iname[0].name})
            insn_dep = sf.interface.realize_direct_output(matprod, output_inames, out_shape, **insn_args)
        elif l == len(matrix_sequence) - 1:
            # Handle output of the last tensor contraction
            #
            # Stage 1: Reverse cost permutation, keep quadrature permutation
            # Stage 3: Reverse cost and quadrature permuation
            output_shape = tuple(out_shape[1:]) + (out_shape[0],)
            output_inames = permute_backward(output_inames, sf.interface.cost_permutation)
            output_shape = permute_backward(output_shape, sf.interface.cost_permutation)
            if sf.interface.stage == 3:
                output_inames = permute_backward(output_inames, sf.interface.quadrature_permutation)
                output_shape = permute_backward(output_shape, sf.interface.quadrature_permutation)

            out = buffer.get_temporary(sf,
                                       "buff_step{}_out".format(l),
                                       shape=output_shape + vec_shape,
                                       dim_tags=ftags,
                                       )

            # Issue the reduction instruction that implements the multiplication
            # at the same time store the instruction ID for the next instruction to depend on
            insn_dep = frozenset({instruction(assignee=prim.Subscript(prim.Variable(out), output_inames + vec_iname),
                                              expression=matprod,
                                              **insn_args
                                              )
                                  })

        else:
            output_shape = tuple(out_shape[1:]) + (out_shape[0],)
            out = buffer.get_temporary(sf,
                                       "buff_step{}_out".format(l),
                                       shape=output_shape + vec_shape,
                                       dim_tags=ftags,
                                       )

            # Issue the reduction instruction that implements the multiplication
            # at the same time store the instruction ID for the next instruction to depend on
            insn_dep = frozenset({instruction(assignee=prim.Subscript(prim.Variable(out), output_inames + vec_iname),
                                              expression=matprod,
                                              **insn_args
                                              )
                                  })

    # Construct a loopy kernel object
    from dune.codegen.pdelab.localoperator import extract_kernel_from_cache
    args = ("const char* buffer0", "const char* buffer1") + sf.interface.signature_args
    signature = "void {}({}) const __attribute__((always_inline))".format(sf.function_name, ", ".join(args))
    kernel = extract_kernel_from_cache("kernel_default", sf.function_name, [signature], add_timings=False)
    delete_cache_items("kernel_default")
    return kernel
