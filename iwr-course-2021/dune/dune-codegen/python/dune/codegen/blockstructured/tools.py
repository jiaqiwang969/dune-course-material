from dune.codegen.tools import get_pymbolic_basename
from dune.codegen.generation import (iname,
                                     domain,
                                     temporary_variable,
                                     instruction, globalarg, preamble)
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.options import get_form_option
import pymbolic.primitives as prim


# add inames over the micro elements in tensor representation,
# i.e. each element has (i_1,i_2,...,i_d) indices
@iname
def sub_element_inames():
    name = "subel"
    dim = world_dimension()
    dim_names = ["x", "y", "z"] + [str(i) for i in range(4, dim + 1)]
    inames = tuple()
    for i in range(dim):
        inames = inames + ("subel_" + dim_names[i],)
        domain("subel_" + dim_names[i], get_form_option("number_of_blocks"))
    return inames


def remove_sub_element_inames(indices):
    assert isinstance(indices, tuple)
    return tuple(set(indices) - set(sub_element_inames()) - set(prim.Variable(i) for i in sub_element_inames()))


# compute sequential index for given tensor index, the same as index in base-k to base-10
def tensor_index_to_sequential_index(indices, k):
    return prim.Sum(tuple(prim.Variable(index) * k ** i for i, index in enumerate(indices)))


# compute tensor index for given sequential index, the same as index in base-10 to base-k
def sequential_index_to_tensor_index(iname, k):
    return tuple(prim.Remainder(prim.Variable(iname) / (k**i), k) for i in range(world_dimension()))


# compute index for higher order FEM for a given Q1 index
def micro_index_to_macro_index(element, inames):
    subelem_inames = sub_element_inames()

    k = get_form_option("number_of_blocks")
    p = element.degree()
    return prim.Sum(tuple((p * prim.Variable(si) + prim.Variable(bi)) * (p * k + 1) ** i
                          for i, (si, bi) in enumerate(zip(subelem_inames, inames))))


# translate a point in the micro element into macro coordinates
def define_point_in_macro(name, point_in_micro, visitor):
    # TODO this won't work for 2d mannifolds
    dim = world_dimension()
    if get_form_option('vectorization_blockstructured'):
        temporary_variable(name, shape=(dim,), managed=True)
    else:
        temporary_variable(name, shape=(dim,), shape_impl=('fv',))

    # point_macro = (point_micro + index_micro) / number_of_blocks
    # where index_micro = tensor index of the micro element
    subelem_inames = sub_element_inames()
    for i in range(dim):
        if isinstance(point_in_micro, prim.Subscript):
            expr = prim.Subscript(point_in_micro.aggregate, point_in_micro.index + (i,))
        else:
            expr = prim.Subscript(point_in_micro, (i,))
        expr = prim.Sum((expr, prim.Variable(subelem_inames[i]),))
        expr = prim.Quotient(expr, get_form_option('number_of_blocks'))
        instruction(assignee=prim.Subscript(prim.Variable(name), (i,)),
                    expression=expr,
                    within_inames=frozenset(visitor.quadrature_inames()),
                    tags=frozenset(subelem_inames)
                    )


def name_point_in_macro(point_in_micro, visitor):
    assert isinstance(point_in_micro, prim.Expression)
    name = get_pymbolic_basename(point_in_micro) + "_macro"
    define_point_in_macro(name, point_in_micro, visitor)
    return name


@preamble
def define_container_alias(name, container, lfs, element, is_const):
    k = get_form_option("number_of_blocks")
    p = element.degree()
    dim = world_dimension()
    element_stride = tuple(p * (p * k + 1)**i for i in range(0, dim))
    index_stride = tuple((p * k + 1)**i for i in range(0, dim))
    globalarg(name, shape=(k,) * dim + (p + 1,) * dim, strides=element_stride + index_stride, managed=True)
    if is_const:
        return "const auto {} = &{}({},0);".format(name, container, lfs.name)
    else:
        return "auto {} = &{}.container()({},0);".format(name, container, lfs.name)


def name_accumulation_alias(container, accumspace):
    name = container + "_" + accumspace.lfs.name + "_alias"
    name_tail = container + "_" + accumspace.lfs.name + "_alias_tail"

    define_container_alias(name, container, accumspace.lfs, accumspace.element, is_const=False)
    define_container_alias(name_tail, container, accumspace.lfs, accumspace.element, is_const=False)
    return name


def name_container_alias(container, lfs, element):
    name = container + "_" + lfs.name + "_alias"

    define_container_alias(name, container, lfs, element, is_const=True)
    return name
