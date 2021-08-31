""" Generator functions for PDELab local/grid function spaces etc. """

from dune.codegen.generation import (class_member,
                                     domain,
                                     function_mangler,
                                     generator_factory,
                                     include_file,
                                     kernel_cached,
                                     preamble,
                                     valuearg,
                                     )
from dune.codegen.pdelab.localoperator import (lop_template_ansatz_gfs,
                                               lop_template_test_gfs,
                                               name_coefficient_gfs,
                                               name_coefficient_lfs,
                                               type_gridfunctionspace_template_parameter,
                                               )
from dune.codegen.pdelab.restriction import restricted_name
from dune.codegen.pdelab.geometry import name_cell
from dune.codegen.ufl.modified_terminals import Restriction

from loopy import CallMangleInfo
from loopy.symbolic import FunctionIdentifier
from loopy.types import NumpyType

from pymbolic.primitives import Variable
from functools import partial
import numpy


def name_lfs_bound(lfs):
    bound = '{}_size'.format(lfs)
    return bound


@preamble
def using_indices():
    return "using namespace Dune::Indices;"


@generator_factory(cache_key_generator=lambda e, r, **kw: (e, r))
def name_leaf_lfs(leaf_element, restriction, val=None):
    """ This function just caches leaf lfs names based on the
    element. The resulting local function spaces are useful only
    for size information. OTOH, they are available with just the
    leaf element available (as seen in basis evaluation).
    """
    assert val
    return val


@generator_factory(cache_key_generator=lambda e, **kw: e)
def type_leaf_gfs(leaf_element, val=None):
    """ This function just caches leaf lfs names based on the
    element. The resulting local function spaces are useful only
    for size information. OTOH, they are available with just the
    leaf element available (as seen in basis evaluation).
    """
    assert val
    return val


@generator_factory(cache_key_generator=lambda e, r, **kw: (e, r))
def available_lfs_names(element, restriction, name=None):
    assert name
    return name


@generator_factory(cache_key_generator=lambda e, r, **kw: e)
def available_gfs_names(element, restriction, name=None):
    assert name
    return name


@preamble
def bind_lfs(name, restriction):
    entity = name_cell(restriction)
    return "{}->bind({});".format(name, entity)


@preamble
def define_lfs(name, father, child, restriction):
    using_indices()
    bound = name_lfs_bound(name)
    return "auto {} = child({}, _{});".format(name, father, child)


def define_lfs_size(lfs, element, restriction):
    name = name_lfs_bound(lfs)
    valuearg(name, dtype=numpy.int32)
    _define_lfs_size(name, lfs, restriction)


@preamble
def _define_lfs_size(name, lfs, restriction):
    return "auto {} = {}.size();".format(name, lfs)


@class_member(classtag="operator")
def define_gfs(name, father, child):
    include_file("dune/typetree/childextraction.hh", filetag="operatorfile")
    return 'using {} = Dune::TypeTree::Child<{},{}>;'.format(name, father, child)


def _name_lfs(element, restriction, tp, name):
    if len(tp) == 0:
        name_leaf_lfs(element, restriction, val=name)
        define_lfs_size(name, element, restriction)
        return name

    childname = "{}_{}".format(name, tp[0])
    define_lfs(childname, name, tp[0], restriction)
    return _name_lfs(element.sub_elements()[tp[0]], restriction, tp[1:], childname)


def _type_gfs(element, restriction, tp, name):
    if len(tp) == 0:
        type_leaf_gfs(element, val=name)
        return name

    childname = "{}_{}".format(name, tp[0])
    define_gfs(childname, name, tp[0])
    return _type_gfs(element.sub_elements()[tp[0]], restriction, tp[1:], childname)


def _function_space_traversal(element, restriction, index, defaultname=None, recfunc=None):
    """Traverse a function space. This could be done for generating the name of lfs
    or the type of a gfs.
    """
    name = defaultname(element, restriction)
    tp = ()
    from ufl import MixedElement
    if isinstance(element, MixedElement):
        assert index is not None
        tp = element.extract_subelement_component(index)
        tp = (tp[0],) + tp[1]

    return recfunc(element, restriction, tp, name)


name_lfs = partial(_function_space_traversal, defaultname=available_lfs_names, recfunc=_name_lfs)
type_gfs = partial(_function_space_traversal, defaultname=available_gfs_names, recfunc=_type_gfs)


@preamble
def define_dereference_name(name, pointer_name):
    return "auto& {} = * {};".format(name, pointer_name)


def dereference_name(pointer_name):
    name = "deref_" + pointer_name
    define_dereference_name(name, pointer_name)
    return name


@kernel_cached
def initialize_function_spaces(expr, restriction, indices):
    index = None
    from ufl import MixedElement
    if isinstance(expr.ufl_element(), MixedElement):
        index = indices[0]

    from ufl.classes import Argument, Coefficient
    if isinstance(expr, Argument) and expr.number() == 0:
        lfs_name = name_testfunctionspace(restriction)
        gfs_type = lop_template_test_gfs()
    elif isinstance(expr, Coefficient) and expr.count() > 2:
        lfs_pointer_name = name_coefficient_lfs(expr, restriction)
        lfs_name = dereference_name(lfs_pointer_name)
        gfs_type = type_gridfunctionspace_template_parameter(expr)
    else:
        lfs_name = name_trialfunctionspace(restriction)
        gfs_type = lop_template_ansatz_gfs()

    # Local function space
    available_lfs_names(expr.ufl_element(),
                        restriction,
                        name=lfs_name)
    name_lfs(expr.ufl_element(), restriction, index)

    # Grid function space
    available_gfs_names(expr.ufl_element(), 0,
                        name=gfs_type)
    type_gfs(expr.ufl_element(), restriction, index)


@generator_factory(item_tags=("iname",), cache_key_generator=lambda e, r, c: (e, c), context_tags=("kernel",))
def _lfs_iname(element, restriction, context):
    lfs = name_leaf_lfs(element, restriction)
    bound = name_lfs_bound(lfs)

    name = "{}_{}_index".format(lfs, context)
    domain(name, bound)

    return name


def lfs_iname(element, restriction, count=None, context=''):
    """ Get the iname to iterate over the local function space given by element

    Arguments:
    ----------
    element: ufl.FiniteElementBase
        The finite element this local function space belongs to
    argcount: int
        Use to realize double nesting in case of jacobians
    context: str
        Some generation methods will require you to duplicate an iname for
        a given purpose, see the 'Loops and dependencies' of the loopy docs:
        https://documen.tician.de/loopy/tutorial.html#loops-and-dependencies
    """
    assert not ((context == '') and (count is None))
    if count is not None:
        if context != '':
            context = "{}_{}".format(count, context)
        else:
            context = str(count)
    return _lfs_iname(element, restriction, context)


def lfs_inames(element, restriction, count=None, context=''):
    return (lfs_iname(element, restriction, count, context),)


def name_testfunctionspace(restriction):
    return restricted_name("lfsv", restriction)


def name_trialfunctionspace(restriction):
    return restricted_name("lfsu", restriction)


def type_testfunctionspace():
    return "LFSV"


def type_trialfunctionspace():
    return "LFSU"
