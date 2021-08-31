from dune.codegen.generation import domain
from dune.codegen.pdelab.geometry import world_dimension
from dune.codegen.pdelab.spaces import name_leaf_lfs


def lfs_inames(element, restriction, count=None, context=''):
    assert not ((context == '') and (count is None))
    if context == '':
        context = "test"
    if count is not None:
        context = "{}_{}".format(count, context)

    lfs = name_leaf_lfs(element, restriction)

    # register transformation
    # warning: this will register the transformation a couple of times
    from dune.codegen.generation import transform
    from dune.codegen. blockstructured.transformations import blockstructured_iname_duplication
    transform(blockstructured_iname_duplication)

    dim_names = ["x", "y", "z"] + [str(i) for i in range(4, world_dimension() + 1)]
    name = "micro_{}_{}_index_".format(lfs, context)
    inames = tuple()
    for i in range(world_dimension()):
        inames = inames + (name + dim_names[i],)
        domain(name + dim_names[i], element.degree() + 1)
    return inames
