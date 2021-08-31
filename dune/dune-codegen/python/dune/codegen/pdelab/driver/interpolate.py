"""Create grid functions

Create all kinds of grid functions. This includes grid functions for the
boundary condition ('interpolate expression') the exact solution
('exact_solution') and the grid function that decides where Dirichlet boundary
conditions are applied ('is_dirichlet')
"""


from dune.codegen.generation import (cached,
                                     class_member,
                                     get_counted_variable,
                                     global_context,
                                     include_file,
                                     preamble,
                                     )
from dune.codegen.pdelab.driver import (FEM_name_mangling,
                                        get_form_ident,
                                        get_trial_element,
                                        is_stationary,
                                        preprocess_leaf_data,
                                        )
from dune.codegen.pdelab.driver.driverblock import (grid_function_identifier,
                                                    name_driver_block,
                                                    type_driver_block)
from dune.codegen.pdelab.driver.gridfunctionspace import (name_trial_gfs,
                                                          name_leafview,
                                                          type_leafview,
                                                          type_range,
                                                          )
from ufl import FiniteElement, MixedElement, TensorElement, VectorElement, TensorProductElement


@preamble(section="vector", kernel="driver_block")
def interpolate_vector(func, gfs, name):
    return "Dune::PDELab::interpolate(*{}, *{}, *{});".format(func,
                                                              gfs,
                                                              name,
                                                              )


def interpolate_dirichlet_data(name):
    identifier = "interpolate_expression"
    element = get_trial_element()
    func = preprocess_leaf_data(element, grid_function_identifier(identifier), applyZeroDefault=False)
    if func is not None:
        bf = name_grid_function_root(identifier)
        gfs = name_trial_gfs()
        interpolate_vector(bf, gfs, name)


def _grid_function_root_type(identifier):
    name_dict = {"exact_solution": "ExactSolution",
                 "interpolate_expression": "BoundaryGridFunction",
                 "is_dirichlet": "BoundaryConditionType"}
    return name_dict[identifier]


def _grid_function_root_name(identifier):
    name_dict = {"exact_solution": "exactSolution",
                 "interpolate_expression": "boundaryGridFunction",
                 "is_dirichlet": "boundaryConditionType"}
    return name_dict[identifier]


def _get_grid_function_method_name(identifier):
    name_dict = {"exact_solution": "getExactSolution",
                 "interpolate_expression": "getBoundaryGridFunction",
                 "is_dirichlet": "getBoundaryConditionType"}

    return name_dict[identifier]


#
# Composite grid function
#


@class_member(classtag="driver_block")
def typedef_composite_grid_function(name, identifier, children):
    templates = ','.join('std::decay_t<decltype(*{})>'.format(c) for c in children)
    if identifier == "is_dirichlet":
        composite_type = "Dune::PDELab::CompositeConstraintsParameters"
    else:
        composite_type = "Dune::PDELab::CompositeGridFunction"
    return "using {} = {}<{}>;".format(name, composite_type, templates)


def type_composite_grid_function(identifier, children, root):
    if root:
        name = _grid_function_root_type(identifier)
    elif identifier == "is_dirichlet":
        name = "CompositeConstraintsParameters_{}".format('_'.join(c for c in children))
    else:
        name = "CompositeGridFunction_{}".format('_'.join(c for c in children))
    typedef_composite_grid_function(name, identifier, children)
    return name


@class_member(classtag="driver_block")
def declare_composite_grid_function(identifier, name, children, root):
    composite_gfs_type = type_composite_grid_function(identifier, children, root)
    return "std::shared_ptr<{}> {};".format(composite_gfs_type, name)


@preamble(section="gridfunction", kernel="driver_block")
def define_composite_grid_function(identifier, name, children, root=True):
    declare_composite_grid_function(identifier, name, children, root)
    composite_gfs_type = type_composite_grid_function(identifier, children, root)
    return "{} = std::make_shared<{}>({});".format(name, composite_gfs_type, ', '.join('*{}'.format(c) for c in children))


#
# Function used to generate grid function
#


def function_lambda(func):
    assert isinstance(func, tuple)
    func = func[0]
    if func is None:
        func = 0.0

    if isinstance(func, (int, float)):
        return "[&](const auto& is, const auto& xl){{ return {}; }}".format(float(func))
    else:
        from ufl.classes import Expr
        assert isinstance(func, Expr)
        from dune.codegen.pdelab.driver.visitor import ufl_to_code
        return "[&](const auto& is, const auto& xl){{ {}; }}".format(ufl_to_code(func))


@class_member(classtag="driver_block")
def typedef_function(name, boolean=False):
    leafview_type = type_leafview()
    if boolean:
        return_type = "bool"
        entity = "typename {}::Intersection".format(leafview_type)
        coordinate = "typename {}::Intersection::LocalCoordinate".format(leafview_type)
    else:
        return_type = type_range()
        entity = "typename {}::template Codim<0>::Entity".format(leafview_type)
        coordinate = "typename {}::template Codim<0>::Entity::Geometry::LocalCoordinate".format(leafview_type)
    return "using {} = std::function<{}({}, {})>;".format(name, return_type, entity, coordinate)


def type_function(boolean):
    if boolean:
        name = "BoolFunctionExpression"
        boolean = True
    else:
        name = "FunctionExpression"
        boolean = False
    typedef_function(name, boolean=boolean)
    return name


@class_member(classtag="driver_block")
def declare_function(name, boolean):
    function_type = type_function(boolean)
    return "std::shared_ptr<{}> {};".format(function_type, name)


@preamble(section="gridfunction", kernel="driver_block")
def define_function(name, func, boolean):
    declare_function(name, boolean)
    function_type = type_function(boolean)
    fct_lambda = function_lambda(func)
    return "{} = std::make_shared<{}> ({});".format(name, function_type, fct_lambda)


@cached
def name_function(func, boolean):
    name = get_counted_variable("functionExpression")
    define_function(name, func, boolean)
    return name


#
# Leaf grid function
#


@class_member(classtag="driver_block")
def typedef_grid_function(name, boolean=False):
    leafview_type = type_leafview()
    range_type = type_range()
    function_type = type_function(boolean)
    if boolean:
        return "using {} = Dune::PDELab::LocalCallableToBoundaryConditionAdapter<{}>;".format(name,
                                                                                              function_type)
    elif is_stationary():
        return "using {} = Dune::PDELab::LocalCallableToGridFunctionAdapter<{}, {}, {}, {}>;".format(name,
                                                                                                     leafview_type,
                                                                                                     range_type,
                                                                                                     1,
                                                                                                     function_type)
    else:
        from dune.codegen.pdelab.driver.gridoperator import type_localoperator
        lop_type = type_localoperator(get_form_ident())
        return "using {} = Dune::PDELab::LocalCallableToInstationaryGridFunctionAdapter" \
            "<{}, {}, {}, {}, {}>;".format(name,
                                           leafview_type,
                                           range_type,
                                           1,
                                           function_type,
                                           lop_type)


def type_grid_function(identifier, root):
    if identifier == "is_dirichlet":
        name = "BoolGridFunctionLeaf"
        boolean = True
    else:
        name = "GridFunctionLeaf"
        boolean = False
    if root:
        name = _grid_function_root_type(identifier)
    typedef_grid_function(name, boolean=boolean)
    return name


@class_member(classtag="driver_block")
def declare_grid_function(identifier, name, root):
    grid_function_type = type_grid_function(identifier, root)
    return "std::shared_ptr<{}> {};".format(grid_function_type, name)


@preamble(section="gridfunction", kernel="driver_block")
def define_grid_function(identifier, name, func, root=True):
    declare_grid_function(identifier, name, root)
    gv = name_leafview()

    if identifier == "is_dirichlet":
        boolean = True
    else:
        boolean = False
    function_name = name_function(func, boolean)

    grid_function_type = type_grid_function(identifier, root)
    include_file('dune/pdelab/function/callableadapter.hh', filetag='driver_block')
    if identifier == "is_dirichlet":
        return "{} = std::make_shared<{}>(*{});".format(name, grid_function_type, function_name)
    elif is_stationary():
        return "{} = std::make_shared<{}>({}, *{});".format(name, grid_function_type, gv, function_name)
    else:
        from dune.codegen.pdelab.driver.gridoperator import name_localoperator
        lop = name_localoperator(get_form_ident())
        return "{} = std::make_shared<{}>({}, *{}, *{});".format(name, grid_function_type, gv, function_name, lop)


def name_grid_function(identifier, element, func, root=True):
    assert isinstance(func, tuple)

    if isinstance(element, MixedElement):
        k = 0
        childs = []
        for subel in element.sub_elements():
            childs.append(name_grid_function(identifier, subel, func[k:k + subel.value_size()], root=False))
            k = k + subel.value_size()
        name = "_".join(childs)
        if len(childs) == 1:
            name = "{}_dummy".format(name)
        if root:
            name = identifier
        define_composite_grid_function(identifier, name, tuple(childs), root=root)
    else:
        assert isinstance(element, (FiniteElement, TensorProductElement))
        name = get_counted_variable(identifier)
        if root:
            name = identifier
        define_grid_function(identifier, name, func, root=root)
    return name


#
# Name of root of grid function
#

@cached
def name_grid_function_root(identifier):
    element = get_trial_element()
    func = preprocess_leaf_data(element, grid_function_identifier(identifier))
    name = name_grid_function(identifier, element, func, root=True)
    return name


#
# Use grid function outside the driver block
#


@preamble(section="driverblock", kernel="main")
def main_typedef_grid_function(name, identifier, treepath):
    if len(treepath) == 0:
        driver_block_type = type_driver_block()
        gf_type = _grid_function_root_type(identifier)
        type_name = "{}::{}".format(driver_block_type, gf_type)
    else:
        root_type = main_type_grid_function(identifier, ())
        type_name = "Dune::TypeTree::Child<{}, {}>;".format(root_type, ", ".join(str(t) for t in treepath))
    return "using {} = {};".format(name, type_name)


def main_type_grid_function(identifier, treepath):
    name = _grid_function_root_type(identifier)
    if len(treepath) > 0:
        name = "{}_{}".format(name, "_".join(str(t) for t in treepath))
    main_typedef_grid_function(name, identifier, treepath)
    return name


@class_member(classtag="driver_block")
def driver_block_get_grid_function(identifier, name=None):
    if not name:
        name = name_grid_function_root(identifier)
    gf_type = _grid_function_root_type(identifier)
    method_name = _get_grid_function_method_name(identifier)
    return ["std::shared_ptr<{}> {}(){{".format(gf_type, method_name),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_grid_function(name, identifier, treepath):
    if len(treepath) == 0:
        driver_block_get_grid_function(identifier)
        driver_block_name = name_driver_block()
        method_name = _get_grid_function_method_name(identifier)
        return "auto {} = {}.{}();".format(name, driver_block_name, method_name)
    else:
        root_name = main_name_grid_function(identifier, ())
        indices = ["Dune::Indices::_{}".format(str(t)) for t in treepath]
        return "auto {} = child(*{}, {});".format(name, root_name, ", ".join(i for i in indices))


def main_name_grid_function(identifier, treepath=()):
    name = _grid_function_root_name(identifier)
    if len(treepath) > 0:
        name = "{}_{}".format(name, "_".join(str(t) for t in treepath))
    main_define_grid_function(name, identifier, treepath)
    return name
