from collections import Counter

from dune.codegen.generation import(delete_cache_items,
                                    generator_factory,
                                    global_context,
                                    no_caching,
                                    retrieve_cache_functions,
                                    retrieve_cache_items,
                                    )


def print_cache():
    """Print all cache items"""
    for i in retrieve_cache_items("True"):
        print(i)


# ================================================
# Test retrieve_cache_items and delete_cache_items
# ================================================


# Some generators
gen_foo = generator_factory(item_tags=("foo",))
gen_bar = generator_factory(item_tags=("bar",))
gen_foobar = generator_factory(item_tags=("foo", "bar"))


# Some decorated functions
@gen_foo
def foo(name):
    return "foo {}".format(name)


@gen_bar
def bar(name):
    return "bar {}".format(name)


@gen_foobar
def foobar(name):
    return "foobar {}".format(name)


# Will add two cache entries one with tag foo and one with tag bar
@gen_foo
@gen_bar
def foobar_two(name):
    return "foobar_two {}".format(name)


def setup_cache():
    """Empty cache and fill it in a specific way

    After calling this function the cache will be filled with the
    following entries:

    foo foo (tag foo)
    foobar_two foobar_two_1 (tag foo)
    bar bar_1 (tag bar)
    bar bar_2 (tag bar)
    foobar_two foobar_two_1 (tag bar)
    foobar foobar (tag foo and bar)

    """
    delete_cache_items()
    assert not list(retrieve_cache_items("True"))

    foo("foo")
    bar("bar_1")
    bar("bar_2")
    foobar("foobar")
    foobar_two("foobar_two")

    # This call shouldn't change anything
    foo("foo")

    # print_cache()


# Some lists for comparison
# Empty
list_empty = []
list_not_foo_not_bar = []


# One field
list_foo_not_bar = ["foo foo", "foobar_two foobar_two"]
list_not_foo_and_bar = ["bar bar_1", "bar bar_2", "foobar_two foobar_two"]
list_foo_and_bar = ["foobar foobar"]


# Two fields
list_foo = list_foo_not_bar + list_foo_and_bar
list_bar = list_not_foo_and_bar + list_foo_and_bar
list_not_foobar = list_foo_not_bar + list_not_foo_and_bar


# All three fields
list_foo_or_bar = list_foo_not_bar + list_not_foo_and_bar + list_foo_and_bar
list_full = list_foo_or_bar


def compare(x, y):
    """Compare if lists x and y have the same entries

    Having the same entries means:

    - If item a can be found k times in x it must also be k times in y
    - Vice versa.
    - Ordering of items doesn't matter.
    """
    return Counter(x) == Counter(y)


def test_retrieve_cache():
    """Test all combinations of retrieve_cache for our test setup"""
    # Setup cache in the way descibed above
    setup_cache()

    # Empty
    assert compare(list_empty, list(retrieve_cache_items("False")))
    assert compare(list_not_foo_not_bar, list(retrieve_cache_items("not foo and not bar")))

    # One field
    assert compare(list_foo_not_bar, list(retrieve_cache_items("foo and not bar")))
    assert compare(list_not_foo_and_bar, list(retrieve_cache_items("not foo and bar")))
    assert compare(list_foo_and_bar, list(retrieve_cache_items("foo and bar")))

    # Two fields
    assert compare(list_foo, list(retrieve_cache_items("foo")))
    assert compare(list_bar, list(retrieve_cache_items("bar")))
    assert compare(list_not_foobar, list(retrieve_cache_items("not (foo and bar)")))

    # All three fields
    assert compare(list_foo_or_bar, list(retrieve_cache_items("foo or bar")))
    assert compare(list_full, list(retrieve_cache_items("True")))


def test_delete_cache_items():
    """Test all combinations of delete_cache_items for our test setup"""

    # Tests deleting "all three fields"
    setup_cache()
    delete_cache_items("True")
    assert compare(list_empty, list(retrieve_cache_items("True")))

    setup_cache()
    delete_cache_items("foo or bar")
    assert compare(list_not_foo_not_bar, list(retrieve_cache_items("True")))

    # Tests deleting "two fields"
    setup_cache()
    delete_cache_items("bar")
    assert compare(list_foo_not_bar, list(retrieve_cache_items("True")))

    setup_cache()
    delete_cache_items("foo")
    assert compare(list_not_foo_and_bar, list(retrieve_cache_items("True")))

    setup_cache()
    delete_cache_items("(foo and not bar) or (not foo and bar)")
    assert compare(list_foo_and_bar, list(retrieve_cache_items("True")))

    # Tests deleting "one field"
    setup_cache()
    delete_cache_items("not foo and bar")
    assert compare(list_foo, list(retrieve_cache_items("True")))

    setup_cache()
    delete_cache_items("foo and not bar")
    assert compare(list_bar, list(retrieve_cache_items("True")))

    setup_cache()
    delete_cache_items("foo and bar")
    assert compare(list_not_foobar, list(retrieve_cache_items("True")))

    # Tests deleting nothing
    setup_cache()
    delete_cache_items("not foo and not bar")
    assert compare(list_foo_or_bar, list(retrieve_cache_items("True")))

    setup_cache()
    delete_cache_items("False")
    assert compare(list_full, list(retrieve_cache_items("True")))


# ===============
# Test no caching
# ===============


@generator_factory(item_tags=("no_caching",), cache_key_generator=no_caching)
def no_caching_function(name):
    return "{}".format(name)


def test_no_caching_function():
    delete_cache_items()
    no_caching_function("one")
    assert compare(["one"], list(retrieve_cache_items("no_caching")))
    no_caching_function("one")
    assert compare(["one", "one"], list(retrieve_cache_items("no_caching")))
    no_caching_function("two")
    assert compare(["one", "one", "two"], list(retrieve_cache_items("no_caching")))


# =====================
# Test multiple kernels
# =====================


def test_multiple_kernels_1():
    preamble = generator_factory(item_tags=("preamble",), context_tags=("kernel",))

    @preamble(kernel="k1")
    def pre1():
        return "blubb"

    @preamble(kernel="k2")
    def pre2():
        return "bla"

    pre1()
    pre2()

    preambles = [p for p in retrieve_cache_items("preamble")]
    assert len(preambles) == 2

    k1, = retrieve_cache_items("k1")
    assert k1 == "blubb"

    k2, = retrieve_cache_items("k2")
    assert k2 == "bla"

    delete_cache_items()


def test_multiple_kernels_2():
    preamble = generator_factory(item_tags=("preamble",), context_tags=("kernel",))

    @preamble(kernel="k1")
    def pre1():
        return "blubb"

    @preamble(kernel="k2")
    def pre2():
        pre1()
        return "bla"

    pre2()

    preambles = [p for p in retrieve_cache_items("preamble")]
    assert len(preambles) == 2

    k1, = retrieve_cache_items("k1")
    assert k1 == "blubb"

    k2, = retrieve_cache_items("k2")
    assert k2 == "bla"

    delete_cache_items()


def test_multiple_kernels_3():
    gen = generator_factory(item_tags=("tag",), context_tags=("kernel",), no_deco=True)

    gen("foo", kernel="k1")
    gen("bar", kernel="k2")

    assert len([i for i in retrieve_cache_items("tag")]) == 2

    k1, = retrieve_cache_items("k1")
    assert k1 == "foo"

    k2, = retrieve_cache_items("k2")
    assert k2 == "bar"

    delete_cache_items()
