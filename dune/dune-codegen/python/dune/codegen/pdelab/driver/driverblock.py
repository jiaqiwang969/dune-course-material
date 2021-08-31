from dune.codegen.generation import (class_basename,
                                     class_member,
                                     constructor_parameter,
                                     initializer_list,
                                     preamble,
                                     template_parameter,
                                     )
from dune.codegen.options import (get_driverblock_option,
                                  get_option,
                                  )
from dune.codegen.pdelab.driver import (get_form_ident,
                                        name_initree,
                                        )


def grid_function_identifier(identifier):
    assert identifier in ["is_dirichlet", "interpolate_expression", "exact_solution"]
    driver_block = get_option("driver_block_to_build")
    if driver_block is None:
        return identifier
    else:
        identifier = get_driverblock_option(identifier)
        assert identifier is not None
        return identifier


@template_parameter(classtag="driver_block")
def driver_block_template_parameter():
    from dune.codegen.pdelab.driver.gridfunctionspace import type_leafview
    return type_leafview()


@class_member(classtag="driver_block")
def driver_block_grid_view():
    from dune.codegen.pdelab.driver.gridfunctionspace import name_leafview, type_leafview
    return "{} {};".format(type_leafview(), name_leafview())


def init_driver_block():
    from dune.codegen.pdelab.driver.gridfunctionspace import name_leafview, type_leafview
    driver_block_template_parameter()
    gridview_argument = "_{}".format(name_leafview())
    constructor_parameter("{}&".format(type_leafview()), gridview_argument, classtag="driver_block")
    constructor_parameter("Dune::ParameterTree", name_initree(), classtag="driver_block")
    initializer_list(name_leafview(), [gridview_argument], classtag="driver_block")
    driver_block_grid_view()


@class_basename(classtag="driver_block")
def driver_block_basename():
    name = get_driverblock_option("classname")
    assert name is not None
    init_driver_block()
    return name


def type_driver_block():
    from dune.codegen.pdelab.driver.gridfunctionspace import type_leafview
    return "{}<{}>".format(driver_block_basename(), type_leafview())


@preamble(section="driverblock", kernel="main")
def define_driver_block(name):
    from dune.codegen.pdelab.driver.gridfunctionspace import name_leafview
    driver_block_type = type_driver_block()
    return "{} {}({}, {});".format(driver_block_type, name, name_leafview(), name_initree())


def name_driver_block():
    db = get_option("driver_block_to_build")

    # This means that this function was called during driver generation. This
    # means there should exactly one driver block specified in the options
    # (possibly with default values everywhere)
    if db is None:
        driver_blocks = [i.strip() for i in get_option("driver_blocks").split(",")]
        assert len(driver_blocks) == 1
        db = driver_blocks[0]
    name = "driverBlock{}".format(db.capitalize())
    define_driver_block(name)
    return name
