""" Context managers for code generation. """

_global_context_cache = {}


class _GlobalContext(object):
    def __init__(self, **kwargs):
        self.kw = kwargs

    def __enter__(self):
        self.old_kw = {}
        for k, v in self.kw.items():
            # First store existing values of the same keys
            if k in _global_context_cache:
                self.old_kw[k] = _global_context_cache[k]
            # Now replace the value with the new one
            _global_context_cache[k] = v

    def __exit__(self, exc_type, exc_value, traceback):
        # Delete all the entries from this context
        for k in self.kw.keys():
            del _global_context_cache[k]
        # and restore previously overwritten values
        for k, v in self.old_kw.items():
            _global_context_cache[k] = v


def global_context(**kwargs):
    return _GlobalContext(**kwargs)


def get_global_context_value(key, default=None):
    return _global_context_cache.get(key, default)


class _CacheRestoringContext(object):
    def __enter__(self):
        from dune.codegen.generation.cache import _generators as g
        self.cache = {}
        for original_func, cache_func in g.items():
            self.cache[original_func] = {}
            for k, v in cache_func._memoize_cache.items():
                self.cache[original_func][k] = v

    def __exit__(self, exc_type, exc_value, traceback):
        from dune.codegen.generation.cache import _generators as g
        for i, c in self.cache.items():
            g[i]._memoize_cache = {}
            for k, v in c.items():
                g[i]._memoize_cache[k] = v


def cache_restoring():
    return _CacheRestoringContext()
