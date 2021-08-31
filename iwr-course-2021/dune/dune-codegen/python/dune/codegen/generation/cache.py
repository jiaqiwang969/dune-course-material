""" This module provides the memoization infrastructure for code
generating functions.
"""
import inspect

from dune.codegen.generation.context import (get_global_context_value,
                                             global_context,
                                             )
from dune.codegen.generation.counter import get_counter
from dune.codegen.options import get_option
from pytools import ImmutableRecord

# Store a global list of generator functions
_generators = {}


def _freeze(data):
    """ A function that deterministically generates an
    immutable item from the given data. Used for cache key generation.
    """
    from collections import Hashable, Iterable, MutableMapping

    # Strings are iterable and hashable, but they do not pose any problems.
    if isinstance(data, str):
        return data

    import ufl.classes
    if isinstance(data, ufl.classes.Expr):
        return data

    from pymbolic.primitives import Expression
    if isinstance(data, Expression):
        return data

    # Check if the given data is already hashable
    if isinstance(data, Hashable):
        if isinstance(data, Iterable):
            return type(data)(_freeze(i) for i in data)
        return data

    # convert standard mutable containers
    if isinstance(data, MutableMapping):
        return tuple((_freeze(k), _freeze(v)) for k, v in data.iteritems())
    if isinstance(data, Iterable):
        return tuple(_freeze(i) for i in data)

    # we don't know how to handle this object, so we give up
    raise TypeError('Cannot freeze non-hashable object {} of type {}'.format(data, type(data)))


def no_caching(*a, **k):
    return get_counter('__no_caching')


class _CacheObject(object):
    """ Data type of objects stored in memoization cache of _RegisteredFunction"""
    def __init__(self, value, count=None):
        self.value = value
        self.count = count
        self.stack = None
        if get_option('debug_cache_with_stack'):
            self.stack = inspect.stack()


class _RegisteredFunction(object):
    """ The data structure for a function that accesses UFL2LoopyDataCache """
    def __init__(self, func,
                 cache_key_generator=lambda *a, **kw: a,
                 counted=False,
                 on_store=lambda x: x,
                 item_tags=(),
                 context_tags=(),
                 section=None,
                 **kwargs
                 ):
        self.func = func
        self.cache_key_generator = cache_key_generator
        self.counted = counted
        self.on_store = on_store
        self.item_tags = item_tags
        self.context_tags = context_tags
        self.kwargs = kwargs
        if section:
            self.item_tags = self.item_tags + (section,)

        # Initialize the memoization cache
        self._memoize_cache = {}

    def _get_content(self, key):
        return self._memoize_cache[key].value

    def __call__(self, *args, **kwargs):
        # Modify the kwargs to include any context tags kept with the generator
        for tag in self.context_tags:
            if tag in self.kwargs and tag not in kwargs:
                kwargs[tag] = self.kwargs[tag]

        # Keep an additional dictionary without context tags
        without_context = {k: v for k, v in kwargs.items() if k not in self.context_tags}

        # Get the cache key from the given arguments
        context_key = tuple(kwargs.get(t, t + "_default") for t in self.context_tags)
        cache_key = self.cache_key_generator(*args, **without_context)
        cache_key = (cache_key, context_key)

        # check whether we have a cache hit
        if cache_key not in self._memoize_cache:
            # evaluate the original function: Once with context tags, once without.
            # Reason: Some generators use their context tag to pass it on to other
            # generators. That should be possible. However, those that do not do this
            # get an unknown keyword...
            try:
                val = self.on_store(self.func(*args, **kwargs))
            except TypeError:
                val = self.on_store(self.func(*args, **without_context))

            # Store cache object
            if self.counted:
                self._memoize_cache[cache_key] = _CacheObject(val, count=get_counter('__cache_counted'))
            else:
                self._memoize_cache[cache_key] = _CacheObject(val)

        # Return the result for immediate usage
        return self._get_content(cache_key)


def generator_factory(**factory_kwargs):
    """ A function decorator factory

    Generates a function decorator, that turns a given function into
    a function that stores its result in a data cache.

    The generated decorator may be used with or without keyword arguments.

    The keyword arguments given to this factory override any keywords
    given to the decorator. This allows the definition of specialized
    decorators for different purposes.

    Possible keyword arguments:
    ---------------------------
    cache_key_generator : function
        A function that maps the arguments of the function to a subset that
        determines whether to use a caches result. The return type is arbitrary,
        as it will be turned immutable by the cache machine afterwards.
        Defaults to identity.
    item_tags : tuple
        A tuple of tags (simple strings) to give to the cache items. Items can be
        retrieved and deleted by tag.
    on_store : function
        A function to apply to the return value of the decorated function
        before storing in the cache. May be used to apply wrappers.
    counted : bool
        Will add a counted tag to the cache item. The type of the stored
        items automatically turns to a tuple with the counttag being the first entry.
    no_deco : bool
        Instead of a decorator, return a function that uses identity as a body.
    context_tags: tuple, str
        A single tag or tuple thereof, that will be added to the cache key. This
        feature can be used to maintain multiple sets of memoized function evaluations,
        for example if you generate multiple loopy kernels at the same time.
    """
    # Tuplize the item_tags parameter
    if "item_tags" in factory_kwargs and isinstance(factory_kwargs["item_tags"], str):
        factory_kwargs["item_tags"] = (factory_kwargs["item_tags"],)
    if "context_tags" in factory_kwargs and isinstance(factory_kwargs["context_tags"], str):
        factory_kwargs["context_tags"] = (factory_kwargs["context_tags"],)

    no_deco = factory_kwargs.pop("no_deco", False)

    def _dec(*args, **kwargs):
        # Modify the kwargs according to the factorys kwargs
        for k in factory_kwargs:
            kwargs[k] = factory_kwargs[k]
        # If there args, this function is used as a decorator, as in this example
        #
        # @decorator
        # def foo():
        #     pass
        #
        # If there are no args, this is used as a decorator factory:
        #
        # @decorator(bar=42)
        # def foo():
        #     pass
        #
        if args:
            assert len(args) == 1
            key = args[0]

            if hasattr(key, "__name__") and key.__name__ == '<lambda>':
                key = str(kwargs)

            funcobj = _generators.setdefault(key, _RegisteredFunction(args[0], **kwargs))
            return lambda *a, **ka: funcobj(*a, **ka)
        else:
            def __dec(f):
                funcobj = _generators.setdefault(f, _RegisteredFunction(f, **kwargs))
                return lambda *a, **ka: funcobj(*a, **ka)
            return __dec

    if no_deco:
        return _dec(lambda x: x)
    else:
        return _dec


# define a decorator 'cached', which may be used as a standard decorator, if no further
# magic is to be added to the caching mechanism
cached = generator_factory(item_tags=("default_cached",))


class _ConditionDict(dict):
    def __init__(self, tags):
        dict.__init__(self)
        self.tags = tags

    def __getitem__(self, i):
        # If we do not add these special cases the dictionary will return False
        # when we execute the following code:
        #
        # eval ("True", _ConditionDict(v.tags)
        #
        # But in this case we want to return True! A normal dictionary
        # would not attempt to replace "True" if "True" is not a
        # key. The _ConditionDict has no such concerns ;).
        if i == "True":
            return True
        if i == "False":
            return False
        return i in self.tags


def _filter_cache_items(gen, condition):
    ret = {}
    for k, v in gen._memoize_cache.items():
        _, context_tags = k
        if eval(condition, _ConditionDict(gen.item_tags + context_tags)):
            ret[k] = v

    return ret


def retrieve_cache_items(condition=True, make_generable=False):
    def as_generable(content):
        if make_generable:
            from cgen import Generable, Line
            if isinstance(content, Generable):
                return content
            if isinstance(content, str):
                return Line(text=content + '\n')
            assert False
        else:
            return content

    # First yield all those items that are not sorted
    for gen in filter(lambda g: not g.counted, _generators.values()):
        for item in _filter_cache_items(gen, condition).values():
            yield as_generable(item.value)

    # And now the sorted ones
    counted_ones = []
    for gen in filter(lambda g: g.counted, _generators.values()):
        counted_ones.extend(_filter_cache_items(gen, condition).values())

    for item in sorted(counted_ones, key=lambda i: i.count):
        from collections import Iterable
        if isinstance(item.value, Iterable) and not isinstance(item.value, str):
            for l in item.value:
                yield as_generable(l)
        else:
            yield as_generable(item.value)


def delete_cache_items(condition=True, keep=False):
    """ Delete items from the cache. """
    if not keep:
        condition = "not ({})".format(condition)

    for gen in _generators.values():
        gen._memoize_cache = _filter_cache_items(gen, condition)


def retrieve_cache_functions(condition="True"):
    return [g.func for g in _generators.values() if eval(condition, _ConditionDict(g.item_tags))]


def inspect_generator(gen):
    # Must be a generator function
    assert(isinstance(gen, _RegisteredFunction))

    print("Inspecting generator function {}".format(gen.func.func_name))
    for k, v in gen._memoize_cache.items():
        print("  args: {}".format(k))
        print("  val:  {}".format(v))
