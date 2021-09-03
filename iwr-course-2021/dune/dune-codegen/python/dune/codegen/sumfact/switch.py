""" boundary and skeleton integrals come in variants in sum factorization - implement the switch! """

import csv

from dune.codegen.generation import (construct_from_mixins,
                                     get_global_context_value,
                                     global_context,
                                     )
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.pdelab.localoperator import generate_kernel, generate_kernels_per_integral
from dune.codegen.pdelab.signatures import (assembly_routine_args,
                                            assembly_routine_signature,
                                            kernel_name,
                                            )
from dune.codegen.options import get_form_option, get_option, form_option_context
from dune.codegen.cgen.clazz import ClassMember


def sumfact_generate_kernels_per_integral(integrals):
    dim = world_dimension()
    measure = get_global_context_value("integral_type")

    if measure == "cell":
        yield generate_kernel(integrals)

    if measure == "exterior_facet":
        # Maybe skip sum factorization on boundary integrals
        if not get_form_option("sumfact_on_boundary"):
            mixin = construct_from_mixins(mixins=[get_form_option("geometry_mixins")])()
            geometry = mixin.nonsumfact_fallback() or get_form_option("geometry_mixins")
            with form_option_context(sumfact=False, geometry_mixins=geometry):
                for k in generate_kernels_per_integral(integrals):
                    yield k
                return

        # Generate all necessary kernels
        for facedir in range(dim):
            for facemod in range(2):
                with global_context(facedir_s=facedir, facemod_s=facemod):
                    yield generate_kernel(integrals)

        # Generate switch statement
        yield generate_exterior_facet_switch()

    if measure == "interior_facet":
        # Generate all necessary kernels
        for facedir_s in range(dim):
            for facemod_s in range(2):
                for facedir_n in range(dim):
                    for facemod_n in range(2):
                        if decide_if_kernel_is_necessary(facedir_s, facemod_s, facedir_n, facemod_n):
                            with global_context(facedir_s=facedir_s, facemod_s=facemod_s, facedir_n=facedir_n, facemod_n=facemod_n):
                                yield generate_kernel(integrals)

        # Generate switch statement
        yield generate_interior_facet_switch()


def get_kernel_name(facedir_s=None, facemod_s=None, facedir_n=None, facemod_n=None):
    with global_context(facedir_s=facedir_s, facemod_s=facemod_s, facedir_n=facedir_n, facemod_n=facemod_n):
        return kernel_name()


def decide_if_kernel_is_necessary(facedir_s, facemod_s, facedir_n, facemod_n):
    # If we are not using YaspGrid, all variants need to be realized
    if get_form_option("geometry_mixins") == "sumfact_multilinear":
        # Reduce the variability according to grid info file
        if get_option("grid_info") is not None:
            filename = get_option("grid_info")
            with open(filename) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=" ")
                for row in csv_reader:
                    if (row[0] == 'skeleton' and
                            facedir_s == int(row[1])) and \
                            (facemod_s == int(row[2])) and \
                            (facedir_n == int(row[3])) and \
                            (facemod_n == int(row[4])):
                        return True
                return False
        else:
            return True

    # The PDELab machineries visit-once policy combined with Yasp avoids any visits
    # with facemod_s being True
    # NB: This is not true anymore for parallel computations, as we would like to
    #     skip computations on the overlap and that requires us to visit intersections
    #     on the right/upper part of the domain from within the domain.
    # if facemod_s:
    #     return False

    # A codim1 entity can never be on the upper resp. lower side of the ref element
    # in both inside and outside cell in a YaspGrid
    if facemod_n == facemod_s:
        return False

    # A codim1 entity has the same orientation in both the embedding in the inside
    # and outside cell for a YaspGrid
    if facedir_n != facedir_s:
        return False

    return True


def generate_exterior_facet_switch():
    # Extract the signature
    signature = assembly_routine_signature()
    args = ", ".join(tuple(a for c, a in assembly_routine_args()))
    dim = world_dimension()

    # Construct the switch statement
    block = []
    block.append("{")
    block.append("  size_t variant = ig.indexInInside();")
    block.append("  switch(variant)")
    block.append("  {")

    for facedir_s in range(dim):
        for facemod_s in range(2):
            block.append("    case {}: {}({}); break;".format(2 * facedir_s + facemod_s,
                                                              get_kernel_name(facedir_s=facedir_s,
                                                                              facemod_s=facemod_s,
                                                                              ),
                                                              args))

    block.append('    default: DUNE_THROW(Dune::Exception, "Variation not implemented.");')
    block.append("  }")
    block.append("}")

    return ClassMember(signature + block)


def generate_interior_facet_switch():
    # Extract the signature
    signature = assembly_routine_signature()
    args = ", ".join(tuple(a for c, a in assembly_routine_args()))
    dim = world_dimension()

    # Construct the switch statement
    block = []
    block.append("{")
    block.append("  size_t variant = ig.indexInOutside() + {} * ig.indexInInside();".format(2 * dim))
    block.append("  switch(variant)")
    block.append("  {")

    for facedir_s in range(dim):
        for facemod_s in range(2):
            for facedir_n in range(dim):
                for facemod_n in range(2):
                    if decide_if_kernel_is_necessary(facedir_s, facemod_s, facedir_n, facemod_n):
                        block.append("    case {}: {}({}); break;".format((2 * facedir_s + facemod_s) * (2 * dim) + 2 * facedir_n + facemod_n,
                                                                          get_kernel_name(facedir_s=facedir_s,
                                                                                          facemod_s=facemod_s,
                                                                                          facedir_n=facedir_n,
                                                                                          facemod_n=facemod_n,
                                                                                          ),
                                                                          args))

    block.append('    default: DUNE_THROW(Dune::Exception, "Variation not implemented.");')
    block.append("  }")
    block.append("}")

    return ClassMember(signature + block)
