""" A kernel transformation that precomputes data and then splits computation
in chunks of vector size independent of divisibility of the loop bounds. """

from dune.codegen.generation import (function_mangler,
                                     include_file,
                                     loopy_class_member,
                                     )
from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.loopy.vcl import get_vcl_type, get_vcl_type_size
from dune.codegen.loopy.transformations.vectorview import (add_vector_view,
                                                           get_vector_view_name,
                                                           )
from dune.codegen.loopy.symbolic import substitute, InplaceCallInstruction
from dune.codegen.tools import get_pymbolic_basename, get_pymbolic_tag, ceildiv
from dune.codegen.options import get_option

from loopy.kernel.creation import parse_domains
from loopy.symbolic import pw_aff_to_expr
from loopy.match import Tagged

from loopy.symbolic import DependencyMapper, IdentityMapper
from pytools import product

import pymbolic.primitives as prim
import loopy as lp
import numpy as np
import re


class TransposeReg(lp.symbolic.FunctionIdentifier):
    def __init__(self,
                 horizontal=1,
                 vertical=1,
                 ):
        self.horizontal = horizontal
        self.vertical = vertical

    def __getinitargs__(self):
        return (self.horizontal, self.vertical)

    @property
    def name(self):
        return "transpose_reg"


@function_mangler
def rotate_function_mangler(knl, func, arg_dtypes):
    if isinstance(func, TransposeReg):
        # This is not 100% within the loopy philosophy, as we are
        # passing the vector registers as references and have them
        # changed. Loopy assumes this function to be read-only.
        include_file("dune/codegen/sumfact/transposereg.hh", filetag="operatorfile")
        vcl = lp.types.NumpyType(get_vcl_type(dtype_floatingpoint(), vector_width=func.horizontal * func.vertical))
        return lp.CallMangleInfo(func.name, (), (vcl,) * func.horizontal)


class VectorIndices(object):
    def __init__(self, suffix):
        self.suffix = suffix
        self.needed = set()

    def get(self, increment):
        name = "vec_index_inc{}{}".format(increment, self.suffix)
        self.needed.add((name, increment))
        return prim.Variable(name)


class AntiPatternRemover(IdentityMapper):
    def map_floor_div(self, expr):
        """ (y + (x % n)) // n -> y // n """
        num = expr.numerator
        den = expr.denominator

        if isinstance(num, prim.Remainder) and num.denominator == den:
            return 0

        if isinstance(num, prim.Sum) and len(num.children) == 2:
            c0, c1 = num.children
            if isinstance(c1, prim.Remainder) and c1.denominator == den:
                return c0 // den

        return IdentityMapper.map_floor_div(self, expr)


def _vectorize_quadrature_loop(knl, inames, suffix):
    #
    # Process/Assert/Standardize the input
    #

    # Construct a match filter for the instructions to handle
    tag = lp.match.Tagged("quadvec")
    within = lp.match.And(tuple(lp.match.Iname(i) for i in inames))
    cond = lp.match.And((tag, within))
    insns = [i for i in lp.find_instructions(knl, cond)]
    if not insns:
        return knl

    # Analyse the inames of the given instructions and identify inames
    # that they all have in common. Those inames will also be iname dependencies
    # of inserted instructions.
    common_inames = frozenset([]).union(*(insn.within_inames for insn in insns)) - frozenset(inames)

    # Determine the vector lane width
    # TODO infer the numpy type here
    vec_size = get_vcl_type_size(dtype_floatingpoint())
    vector_indices = VectorIndices(suffix)

    #
    # Inspect the given instructions for dependent quantities
    # and precompute them
    #

    quantities = []
    for insn in insns:
        for expr in DependencyMapper()(insn.expression):
            quantities.append(get_pymbolic_basename(expr))
    quantities = set(quantities)
    prec_quantities = []

    for quantity in quantities:
        # Check whether there is an instruction that writes this quantity within
        # the given inames. If so, we need a buffer array.
        iname_match = lp.match.And(tuple(lp.match.Iname(i) for i in inames))
        write_match = lp.match.Writes(quantity)
        match = lp.match.And((iname_match, write_match))
        write_insns = lp.find_instructions(knl, match)

        if write_insns:
            # Introduce a substitution rule and find save name
            subst_old = knl.substitutions.keys()
            knl = lp.assignment_to_subst(knl, quantity)
            subst_new = knl.substitutions.keys()
            subst_name, = set(subst_new) - set(subst_old)

            # Do precomputation of the quantity
            prec_quantity = "{}_precomputed".format(quantity)
            prec_quantities.append(prec_quantity)

            knl = lp.precompute(knl, subst_name, inames,
                                temporary_name=prec_quantity,
                                )

            # Enforce memory layout of the precomputation
            tmps = knl.temporary_variables
            tmps[prec_quantity] = tmps[prec_quantity].copy(dim_tags=",".join(["f"] * len(inames)),
                                                           dtype=dtype_floatingpoint())
            knl = knl.copy(temporary_variables=tmps)

            # Introduce a vector view of the precomputation result
            knl = add_vector_view(knl, prec_quantity)

    #
    # Construct a flat loop for the given instructions
    #
    new_insns = []

    size = product(tuple(pw_aff_to_expr(knl.get_iname_bounds(i).size) for i in inames))
    vec_size = get_vcl_type_size(dtype_floatingpoint())
    size = ceildiv(size, vec_size)

    # Add an additional domain to the kernel
    outer_iname = "flat_{}{}".format("_".join(inames), suffix)
    o_domain = "{{ [{0}] : 0<={0}<{1} }}".format(outer_iname, size)
    o_domain = parse_domains(o_domain, {})
    vec_iname = "vec_{}{}".format("_".join(inames), suffix)
    i_domain = "{{ [{0}] : 0<={0}<{1} }}".format(vec_iname, vec_size)
    i_domain = parse_domains(i_domain, {})
    knl = knl.copy(domains=knl.domains + o_domain + i_domain)
    knl = lp.tag_inames(knl, [(vec_iname, "vec")])

    # Update instruction lists
    insns = [i for i in lp.find_instructions(knl, cond)]
    other_insns = [i for i in knl.instructions if i.id not in [j.id for j in insns]]
    quantities = {}
    for insn in insns:
        for expr in DependencyMapper()(insn.expression):
            basename = get_pymbolic_basename(expr)
            quantities.setdefault(basename, frozenset())
            quantities[basename] = quantities[basename].union(frozenset([expr]))

    replacemap = {}

    # Now gather a replacement map for all the quantities
    for quantity, quantity_exprs in quantities.items():
        # This might be a quantity precomputed earlier
        if quantity in prec_quantities:
            for expr in quantity_exprs:
                replacemap[expr] = prim.Subscript(prim.Variable(get_vector_view_name(quantity)), (vector_indices.get(1), prim.Variable(vec_iname)))
        # it might also be the output of a sumfactorization kernel
        elif quantity in knl.temporary_variables:
            tag, = set(get_pymbolic_tag(expr) for expr in quantity_exprs)
            if tag is not None and tag.startswith('vecsumfac'):
                # Extract information from the tag
                horizontal, vertical = tuple(int(i) for i in re.match("vecsumfac_h(.*)_v(.*)", tag).groups())

                # 1. Rotating the input data
                knl = add_vector_view(knl, quantity)
                if horizontal > 1:
                    # Pitfall: In the case of generating jacobians, the input needs to be rotated exactly once.
                    predicates = frozenset()
                    if common_inames:
                        predicates = frozenset({prim.Comparison(prim.Sum(tuple(prim.Variable(i) for i in common_inames)), "==", 0)})

                    assignees = tuple(prim.Subscript(prim.Variable(get_vector_view_name(quantity)),
                                                     (vector_indices.get(horizontal) + i, prim.Variable(vec_iname)))
                                      for i in range(horizontal))
                    new_insns.append(InplaceCallInstruction(assignees,  # assignees
                                                            prim.Call(TransposeReg(vertical=vertical, horizontal=horizontal),
                                                                      assignees),
                                                            within_inames=common_inames.union(frozenset({outer_iname, vec_iname})),
                                                            within_inames_is_final=True,
                                                            id="{}_rotate{}".format(quantity, suffix),
                                                            tags=frozenset({"sumfact_stage2"}),
                                                            predicates=predicates,
                                                            ))

                # Add substitution rules
                for expr in quantity_exprs:
                    assert isinstance(expr, prim.Subscript)
                    last_index = AntiPatternRemover()(expr.index[-1] // vertical)
                    replacemap[expr] = prim.Subscript(prim.Variable(get_vector_view_name(quantity)),
                                                      (vector_indices.get(horizontal) + last_index, prim.Variable(vec_iname)),
                                                      )
            elif tag is not None and tag == 'sumfac':
                # Add a vector view to this quantity
                expr, = quantity_exprs
                knl = add_vector_view(knl, quantity)
                replacemap[expr] = prim.Subscript(prim.Variable(get_vector_view_name(quantity)),
                                                  (vector_indices.get(1), prim.Variable(vec_iname)),
                                                  )
        elif quantity in [a.name for a in knl.args]:
            arg, = [a for a in knl.args if a.name == quantity]
            tags = set(get_pymbolic_tag(expr) for expr in quantity_exprs)
            if tags and tags.pop() == "operator_precomputed":
                expr, = quantity_exprs
                shape = (ceildiv(product(s for s in arg.shape), vec_size), vec_size)
                name = loopy_class_member(quantity,
                                          shape=shape,
                                          dim_tags="f,vec",
                                          potentially_vectorized=True,
                                          classtag="operator",
                                          )
                knl = knl.copy(args=knl.args + [lp.GlobalArg(name, shape=shape, dim_tags="c,vec", dtype=dtype_floatingpoint())])
                replacemap[expr] = prim.Subscript(prim.Variable(name),
                                                  (vector_indices.get(1), prim.Variable(vec_iname)),
                                                  )

    for insn in insns:
        # Get a vector view of the lhs expression
        lhsname = get_pymbolic_basename(insn.assignee)
        knl = add_vector_view(knl, lhsname)
        lhsname = get_vector_view_name(lhsname)
        rotating = "gradvec" in insn.tags

        if rotating:
            assert isinstance(insn.assignee, prim.Subscript)
            tag = get_pymbolic_tag(insn.assignee)
            horizontal, vertical = tuple(int(i) for i in re.match("vecsumfac_h(.*)_v(.*)", tag).groups())
            if horizontal > 1:
                last_index = AntiPatternRemover()(insn.assignee.index[-1] // vertical)
            else:
                last_index = 0
        else:
            last_index = 0
            horizontal = 1

        new_insns.append(lp.Assignment(prim.Subscript(prim.Variable(lhsname),
                                                      (vector_indices.get(horizontal) + last_index, prim.Variable(vec_iname)),
                                                      ),
                                       substitute(insn.expression, replacemap),
                                       depends_on=frozenset({lp.match.Tagged("sumfact_stage1")}),
                                       depends_on_is_final=True,
                                       within_inames=common_inames.union(frozenset({outer_iname, vec_iname})),
                                       within_inames_is_final=True,
                                       id=insn.id,
                                       tags=frozenset({"vec_write{}".format(suffix), "sumfact_stage2"}),
                                       no_sync_with=frozenset({(lp.match.Tagged("sumfact_stage2"), "any")}),
                                       )
                         )

        # Rotate back!
        if rotating and "{}_rotateback{}".format(lhsname, suffix) not in [i.id for i in new_insns] and horizontal > 1:
            assignees = tuple(prim.Subscript(prim.Variable(lhsname),
                                             (vector_indices.get(horizontal) + i, prim.Variable(vec_iname)))
                              for i in range(horizontal))
            new_insns.append(InplaceCallInstruction(assignees,  # assignees
                                                    prim.Call(TransposeReg(horizontal=horizontal, vertical=vertical),
                                                              assignees),
                                                    depends_on=frozenset({Tagged("vec_write{}".format(suffix))}),
                                                    within_inames=common_inames.union(frozenset({outer_iname, vec_iname})),
                                                    within_inames_is_final=True,
                                                    id="{}_rotateback{}".format(lhsname, suffix),
                                                    tags=frozenset({"sumfact_stage2"}),
                                                    ))

    # Add the necessary vector indices
    temporaries = knl.temporary_variables
    for name, increment in vector_indices.needed:
        temporaries[name] = lp.TemporaryVariable(name,  # name
                                                 dtype=np.int32,
                                                 scope=lp.temp_var_scope.PRIVATE,
                                                 )
        new_insns.append(lp.Assignment(prim.Variable(name),  # assignee
                                       0,  # expression
                                       within_inames=common_inames,
                                       within_inames_is_final=True,
                                       id="assign_{}{}".format(name, suffix),
                                       tags=frozenset({"sumfact_stage2"}),
                                       ))
        new_insns.append(lp.Assignment(prim.Variable(name),  # assignee
                                       prim.Sum((prim.Variable(name), increment)),  # expression
                                       within_inames=common_inames.union(frozenset({outer_iname})),
                                       within_inames_is_final=True,
                                       depends_on=frozenset({Tagged("vec_write{}".format(suffix)), "assign_{}{}".format(name, suffix)}),
                                       depends_on_is_final=True,
                                       id="update_{}{}".format(name, suffix),
                                       tags=frozenset({"sumfact_stage2"}),
                                       ))

    from loopy.kernel.creation import resolve_dependencies
    return resolve_dependencies(knl.copy(instructions=new_insns + other_insns,
                                         temporary_variables=temporaries,
                                         ))


def vectorize_quadrature_loop(knl):
    # Loop over the quadrature loops that exist in the kernel.
    # This is implemented very hacky right now...
    from dune.codegen.generation.cache import _generators as _g
    gen = list(filter(lambda i: hasattr(i[0], "__name__") and i[0].__name__ == "_quadrature_inames", _g.items()))[0][1]
    for key, inames in gen._memoize_cache.items():
        element = key[0][0]
        if element is None:
            suffix = ''
        else:
            from dune.codegen.pdelab.driver import FEM_name_mangling
            suffix = "_{}".format(FEM_name_mangling(element))
        knl = _vectorize_quadrature_loop(knl, inames.value, suffix)

    return knl
