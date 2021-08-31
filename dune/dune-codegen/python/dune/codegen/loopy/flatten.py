from loopy.kernel.array import (convert_computed_to_fixed_dim_tags,
                                get_access_info,
                                parse_array_dim_tags,
                                )


class _DummyArrayObject(object):
    def __init__(self, dim_tags):
        self.name = 'isthiseverused'
        self.offset = None
        self.dim_tags = dim_tags

    def num_target_axes(self):
        return 1

    def vector_size(self, target):
        # This should call something on the target instead
        return 1


def flatten_index(index, shape, order="c"):
    """
    A function that flattens a multiindex given the shape
    of the multi dimensional array, a tuple of indices and
    the specification of the axis order ("c" for row major,
    "f" for column major)

    Loopy of course does this automatically in a lot of places.
    This code is only meant to be used if a flat index needs
    to be manually created.
    """
    assert order in ("c", "f")
    assert len(index) == len(shape)

    # Get a tuple of dim tags with the specified order
    dim_tags = parse_array_dim_tags(",".join(order for i in index))

    # Transform them to fixed stride tags
    dim_tags = convert_computed_to_fixed_dim_tags("blubber",  # Name unused
                                                  len(index),  # number of user axes
                                                  1,  # number of implementation axes
                                                  shape,
                                                  dim_tags,
                                                  )
    accinfo = get_access_info(None,  # the target fed into above _DummyArrayObject.vector_size
                              _DummyArrayObject(dim_tags),  # the array duck
                              index,
                              lambda x: x,  # eval_expr, semantics unclear
                              None,  # vectorization info
                              )

    return accinfo.subscripts[0]
