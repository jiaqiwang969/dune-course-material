"""
Class for temporary variables that allows us to use very non-standard types.
"""
from dune.codegen.error import CodegenLoopyError

from loopy import TemporaryVariable

import loopy as lp
import numpy


def _temporary_type(shape_impl, shape, first=True):
    from dune.codegen.loopy.target import type_floatingpoint
    if len(shape_impl) == 0:
        return type_floatingpoint()
    if shape_impl[0] == 'arr':
        if not first or len(set(shape_impl)) != 1:
            raise CodegenLoopyError("We do not allow mixing of C++ containers and plain C arrays, for reasons of mental sanity")
        return type_floatingpoint()
    if shape_impl[0] == 'vec':
        return "std::vector<{}>".format(_temporary_type(shape_impl[1:], shape[1:], first=False))
    if shape_impl[0] == 'fv':
        return "Dune::FieldVector<{}, {}>".format(_temporary_type(shape_impl[1:], shape[1:], first=False), shape[0])
    if shape_impl[0] == 'fm':
        # For now, no field matrices of weird stuff...
        assert len(shape) == 2
        _type = type_floatingpoint()
        return "Dune::FieldMatrix<{}, {}, {}>".format(_type, shape[0], shape[1])


def _default_value(shape_impl, shape):
    assert all([si != "arr" for si in shape_impl])

    if len(shape_impl) == 0:
        return "0.0"

    t = _temporary_type(shape_impl, shape)
    if shape_impl[0] in ['fv', 'fm', 'vec']:
        return "{0}({1})".format(t, _default_value(shape_impl[1:], shape[1:]))


def default_declaration(name, kernel, decl_info):
    shape = kernel.temporary_variables[name].shape
    shape_impl = kernel.temporary_variables[name].shape_impl
    managed = kernel.temporary_variables[name].managed

    # Determine the C++ type to use for this temporary.
    t = _temporary_type(shape_impl, shape)
    if len(shape_impl) == 0:
        # This is a scalar, just return it!
        return '{} {}(0.0);'.format(t, name)

    v = _default_value(shape_impl[1:], shape[1:])
    if shape_impl[0] == 'arr':
        if managed:
            return '{} {}[{}];'.format(t, name, ' * '.join((str(s) for s in shape)))
        else:
            return '{} {}{};'.format(t, name, ''.join('[{}]'.format(s) for s in shape))
    if shape_impl[0] == 'vec':
        return '{} {}({}, {});'.format(t, name, shape[0], v)
    if shape_impl[0] == 'fv':
        return '{} {}({});'.format(t, name, v)
    if shape_impl[0] == 'fm':
        assert len(shape) == 2
        return '{} {}({});'.format(t, name, v)


def custom_base_storage_temporary_declaration(storage):
    def _decl(name, kernel, decl_info):
        dtype = kernel.temporary_variables[name].dtype
        _type = kernel.target.dtype_to_typename(decl_info.dtype)
        return "{0} *{1} = ({0} *){2};".format(_type, name, storage)

    return _decl


class DuneTemporaryVariable(TemporaryVariable):

    allowed_extra_kwargs = TemporaryVariable.allowed_extra_kwargs + ["managed", "shape_impl", "decl_method", "custom_base_storage"]

    def __init__(self, name, managed=False, shape_impl=None, decl_method=None, custom_base_storage=None, **kwargs):
        self.managed = managed
        self.decl_method = decl_method
        self.shape_impl = shape_impl

        if shape_impl is not None:
            self.decl_method = default_declaration

        from dune.codegen.loopy.target import dtype_floatingpoint
        kwargs.setdefault('dtype', dtype_floatingpoint())

        if custom_base_storage and self.decl_method is None:
            assert shape_impl is None
            self.decl_method = custom_base_storage_temporary_declaration(custom_base_storage)

        self.custom_declaration = self.decl_method is not None

        if self.managed and shape_impl is not None:
            for impl in shape_impl:
                assert impl == 'arr'

        TemporaryVariable.__init__(self, name,
                                   managed=self.managed,
                                   shape_impl=self.shape_impl,
                                   decl_method=self.decl_method,
                                   custom_base_storage=custom_base_storage,
                                   **kwargs)
