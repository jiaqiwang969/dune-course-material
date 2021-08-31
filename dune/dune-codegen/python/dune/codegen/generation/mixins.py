""" The infrastructure for registered mixin classes """

from functools import partial


_mixin_registry = {}


def mixin_base(mixintype, name):
    _mixin_registry.setdefault(mixintype, {})

    def _dec(cls):
        _mixin_registry[mixintype][name] = cls
        return cls

    return _dec


def construct_from_mixins(base=object, mixins=[], mixintype="geometry", name="GeometryInterface"):
    mixins = tuple(_mixin_registry[mixintype][m] for m in mixins)
    return type(name, mixins + (base,), {})


# A list of specific mixins that we keep around explicitly
geometry_mixin = partial(mixin_base, "geometry")
quadrature_mixin = partial(mixin_base, "quadrature")
basis_mixin = partial(mixin_base, "basis")
accumulation_mixin = partial(mixin_base, "accumulation")
