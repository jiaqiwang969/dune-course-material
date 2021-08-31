from dune.codegen.generation import kernel_cached

from ufl.classes import MultiIndex, Index


# Now define some commonly used generators that do not fall into a specific category
@kernel_cached
def name_index(index):
    if isinstance(index, Index):
        # This failed for index > 9 because ufl placed curly brackets around
        # return str(index)
        return "i_{}".format(index.count())
    if isinstance(index, MultiIndex):
        assert len(index) == 1
        # return str(index._indices[0])
        return "i_{}".format(index._indices[0].count())
    raise NotImplementedError
