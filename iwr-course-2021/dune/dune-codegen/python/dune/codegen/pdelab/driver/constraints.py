from dune.codegen.generation import (class_member,
                                     get_counted_variable,
                                     global_context,
                                     include_file,
                                     preamble,
                                     )
from dune.codegen.pdelab.driver import (FEM_name_mangling,
                                        get_trial_element,
                                        )
from dune.codegen.pdelab.driver.driverblock import name_driver_block
from dune.codegen.pdelab.driver.gridfunctionspace import (name_leafview,
                                                          name_trial_gfs,
                                                          type_leafview,
                                                          type_range,
                                                          type_trial_gfs,
                                                          preprocess_leaf_data,
                                                          )
from dune.codegen.pdelab.driver.interpolate import name_grid_function_root
from dune.codegen.pdelab.driver.driverblock import grid_function_identifier

from ufl.classes import Expr
from ufl import FiniteElement, MixedElement, TensorElement, VectorElement, TensorProductElement


def name_assembled_constraints():
    name = name_constraintscontainer()
    define_constraintscontainer(name)
    assemble_constraints(name)
    return name


def has_dirichlet_constraints(is_dirichlet):
    if isinstance(is_dirichlet, (tuple, list)):
        return any(has_dirichlet_constraints(d) for d in is_dirichlet)

    if isinstance(is_dirichlet, Expr):
        return True
    else:
        return bool(is_dirichlet)


@preamble(section="constraints", kernel="driver_block")
def assemble_constraints(name):
    element = get_trial_element()
    gfs = name_trial_gfs()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    if has_dirichlet_constraints(is_dirichlet):
        bctype_function = name_grid_function_root("is_dirichlet")
        return "Dune::PDELab::constraints(*{}, *{}, *{});".format(bctype_function,
                                                                  gfs,
                                                                  name,)
    else:
        return "Dune::PDELab::constraints(*{}, *{});".format(gfs,
                                                             name,)


#
# Composite constraints parameters
#


@class_member(classtag="driver_block")
def typedef_composite_constraints_parameters(name, element, gfs_tuple):
    assert isinstance(element, MixedElement)
    assert len(element.sub_elements()) == len(gfs_tuple)
    types = []
    for subel, subgfs in zip(element.sub_elements(), gfs_tuple):
        if isinstance(subel, MixedElement):
            types.append(type_composite_constriants_parameters(subel, subgfs))
        else:
            assert isinstance(subel, (FiniteElement, TensorProductElement))
            types.append(type_bctype_grid_function())
    return "using {} = Dune::PDELab::CompositeConstraintsParameters<{}>;".format(name,
                                                                                 ", ".join(t for t in types))


def type_composite_constriants_parameters(element, gfs_tuple):
    if isinstance(gfs_tuple, str):
        gfs_tuple = (gfs_tuple,)
    name = "CompositeConstraintsParameters_{}".format('_'.join(c for c in gfs_tuple))
    if len(element.sub_elements()) == len(gfs_tuple):
        # If this is not equal the childs have already been typedefed
        typedef_composite_constraints_parameters(name, element, gfs_tuple)
    return name


@class_member(classtag="driver_block")
def declare_composite_constraints_parameter(name, element, gfs_tuple):
    ccp_type = type_composite_constriants_parameters(element, gfs_tuple)
    return "std::shared_ptr<{}> {};".format(ccp_type, name)


@preamble(section="constraints", kernel="driver_block")
def define_composite_constraints_parameters(name, element, gfs_tuple):
    include_file('dune/pdelab/constraints/common/constraintsparameters.hh', filetag='driver_block')
    declare_composite_constraints_parameter(name, element, gfs_tuple)
    ccp_type = type_composite_constriants_parameters(element, gfs_tuple)
    return "{} = std::make_shared<{}>({});".format(name, ccp_type, ', '.join('*{}'.format(c) for c in gfs_tuple))


#
# Constraint container
#


@class_member(classtag="driver_block")
def typedef_constraintscontainer(name):
    gfs = type_trial_gfs()
    r = type_range()
    return "using {} = typename {}::template ConstraintsContainer<{}>::Type;".format(name, gfs, r)


def type_constraintscontainer():
    name = "{}_CC".format(type_trial_gfs())
    typedef_constraintscontainer(name)
    return name


@class_member(classtag="driver_block")
def declare_constraintscontainer(name):
    cctype = type_constraintscontainer()
    return "std::shared_ptr<{}> {};".format(cctype, name)


@preamble(section="constraints", kernel="driver_block")
def define_constraintscontainer(name):
    declare_constraintscontainer(name)
    cctype = type_constraintscontainer()
    return ["{} = std::make_shared<{}>();".format(name, cctype),
            "{}->clear();".format(name)]


def name_constraintscontainer():
    gfs = name_trial_gfs()
    name = "{}_cc".format(gfs)
    element = get_trial_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    define_constraintscontainer(name)
    driver_block_get_constraintscontainer(name=name)
    return name


#
# Export contstraints container
#


@class_member(classtag="driver_block")
def driver_block_get_constraintscontainer(name=None):
    if not name:
        name = name_constraintscontainer()
    constraints_container_type = type_constraintscontainer()
    method_name = "getConstraintsContainer"
    return ["std::shared_ptr<{}> {}(){{".format(constraints_container_type, method_name),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_constraintscontainer(name):
    driver_block_name = name_driver_block()
    driver_block_get_constraintscontainer()
    method_name = "getConstraintsContainer"
    return "auto {} = {}.{}();".format(name, driver_block_name, method_name)


def main_name_constraintscontainer():
    name = "constraintsContainer"
    main_define_constraintscontainer(name)
    return name
