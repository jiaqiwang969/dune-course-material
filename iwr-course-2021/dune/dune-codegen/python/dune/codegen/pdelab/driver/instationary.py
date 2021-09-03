from dune.codegen.generation import (class_member,
                                     include_file,
                                     preamble,
                                     )
from dune.codegen.loopy.target import type_floatingpoint
from dune.codegen.pdelab.driver import (get_trial_element,
                                        is_linear,
                                        name_initree,
                                        preprocess_leaf_data,
                                        )
from dune.codegen.pdelab.driver.driverblock import name_driver_block
from dune.codegen.pdelab.driver.gridfunctionspace import (main_name_trial_gfs,
                                                          type_range,
                                                          )
from dune.codegen.pdelab.driver.gridoperator import (name_gridoperator,
                                                     type_gridoperator,
                                                     main_name_localoperator,
                                                     name_localoperator,
                                                     )
from dune.codegen.pdelab.driver.constraints import (has_dirichlet_constraints,
                                                    main_name_constraintscontainer,
                                                    )
from dune.codegen.pdelab.driver.driverblock import grid_function_identifier
from dune.codegen.pdelab.driver.interpolate import (interpolate_dirichlet_data,
                                                    main_name_grid_function,
                                                    name_grid_function_root,
                                                    )
from dune.codegen.pdelab.driver.solve import (print_matrix,
                                              print_residual,
                                              main_name_vector,
                                              main_type_vector,
                                              name_linearsolver,
                                              name_stationarynonlinearproblemsolver,
                                              name_vector,
                                              type_linearsolver,
                                              type_stationarynonlinearproblemssolver,
                                              type_vector,
                                              )
from dune.codegen.pdelab.driver.vtk import (name_vtk_sequence_writer,
                                            visualize_initial_condition,
                                            name_predicate)
from dune.codegen.options import (get_form_option,
                                  get_option,
                                  get_form_ident,
                                  get_mass_form_ident,
                                  )


def solve_instationary():
    # Create time loop
    if get_form_option('matrix_free'):
        raise NotImplementedError("Instationary matrix free not implemented!")
    else:
        time_loop()
    driverblock_set_time_method()
    print_residual()
    print_matrix()


@class_member(classtag="driver_block")
def driverblock_set_time_method():
    form_ident = get_form_ident()
    lop_name = name_localoperator(form_ident)
    rf = type_floatingpoint()
    return ["void setTime({} t){{".format(rf),
            "  {}->setTime(t);".format(lop_name),
            "}"]


@preamble(section="instat", kernel="main")
def time_loop():
    ini = name_initree()
    lop = main_name_localoperator(get_form_ident())
    time = name_time()
    element = get_trial_element()
    vector_type = main_type_vector(get_form_ident())
    vector = main_name_vector(get_form_ident())
    # interpolate_dirichlet_data(vector)
    gfs = main_name_trial_gfs()

    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    assemble_new_constraints = ""
    if has_dirichlet_constraints(is_dirichlet):
        bctype = main_name_grid_function("is_dirichlet")
        cc = main_name_constraintscontainer()
        # Identation looks strange but is correct in generated C++ file
        assemble_new_constraints = ("  // Assemble constraints for new time step\n"
                                    "      {}->setTime({}+dt);\n"
                                    "      Dune::PDELab::constraints(*{}, *{}, *{});\n"
                                    "".format(lop, time, bctype, gfs, cc)
                                    )

    # Choose between explicit and implicit time stepping
    explicit = get_option('explicit_time_stepping')
    if explicit:
        osm = main_name_onestepmethod(is_implicit=False)
        apply_call = "{}->apply(time, dt, *{}, {}new);".format(osm, vector, vector)
    else:
        osm = main_name_onestepmethod()
    if has_dirichlet_constraints(is_dirichlet):
        boundary = main_name_grid_function("interpolate_expression")
        apply_call = "{}->apply(time, dt, *{}, *{}, {}new);".format(osm, vector, boundary, vector)
    else:
        apply_call = "{}->apply(time, dt, *{}, {}new);".format(osm, vector, vector)

    # Setup visualization
    visualize_initial_condition()
    vtk_sequence_writer = name_vtk_sequence_writer()

    predicate = name_predicate()

    return ["",
            "double T = {}.get<double>(\"instat.T\", 1.0);".format(ini),
            "double dt = {}.get<double>(\"instat.dt\", 0.1);".format(ini),
            "int step_number(0);"
            "int output_every_nth = {}.get<int>(\"instat.output_every_nth\", 1);".format(ini),
            "while (time<T-1e-8){",
            "{}".format(assemble_new_constraints),
            "  // Do time step",
            "  {} {}new(*{});".format(vector_type, vector, vector),
            "  {}".format(apply_call),
            "",
            "  // Accept new time step",
            "  *{} = {}new;".format(vector, vector),
            "  time += dt;",
            "",
            "  step_number += 1;",
            "  if (step_number%output_every_nth == 0){",
            "    // Output to VTK File",
            "    {}.vtkWriter()->clear();".format(vtk_sequence_writer),
            "    Dune::PDELab::addSolutionToVTKWriter(vtkSequenceWriter, *{}, *{},".format(gfs, vector),
            "                                         Dune::PDELab::vtk::defaultNameScheme(), {});".format(predicate),
            "    {}.write({}, Dune::VTK::appendedraw);".format(vtk_sequence_writer, time),
            "  }",
            "}",
            ""]


@preamble(section="init", kernel="main")
def define_time(name):
    return "double {} = 0.0;".format(name)


def name_time():
    define_time("time")
    return "time"


@class_member(classtag="driver_block")
def typedef_timesteppingmethod(name):
    r_type = type_range()
    explicit = get_option('explicit_time_stepping')
    order = get_option('time_stepping_order')
    if explicit:
        if order == 1:
            return "using {} = Dune::PDELab::ExplicitEulerParameter<{}>;".format(name, r_type)
        elif order == 2:
            return "using {} = Dune::PDELab::HeunParameter<{}>;".format(name, r_type)
        elif order == 3:
            return "using {} = Dune::PDELab::Shu3Parameter<{}>;".format(name, r_type)
        elif order == 4:
            return "using {} = Dune::PDELab::RK4Parameter<{}>;".format(name, r_type)
        else:
            raise NotImplementedError("Time stepping method not supported")
    else:
        if order == 1:
            return "using {} = Dune::PDELab::OneStepThetaParameter<{}>;".format(name, r_type)
        elif order == 2:
            return "using {} = Dune::PDELab::Alexander2Parameter<{}>;".format(name, r_type)
        elif order == 3:
            return "using {} = Dune::PDELab::Alexander3Parameter<{}>;".format(name, r_type)


def type_timesteppingmethod():
    typedef_timesteppingmethod("TSM")
    return "TSM"


@class_member(classtag="driver_block")
def declare_timesteppingmethod(name):
    tsm_type = type_timesteppingmethod()
    return "std::shared_ptr<{}> {};".format(tsm_type, name)


@preamble(section="instat", kernel="driver_block")
def define_timesteppingmethod(name):
    declare_timesteppingmethod(name)
    tsm_type = type_timesteppingmethod()
    explicit = get_option('explicit_time_stepping')
    if explicit:
        return "{} = std::make_shared<{}>();".format(name, tsm_type)
    else:
        order = get_option('time_stepping_order')
        if order == 1:
            ini = name_initree()
            return "{} = std::make_shared<{}>({}.get<double>(\"instat.theta\",1.0));".format(name, tsm_type, ini)
        else:
            return "{} = std::make_shared<{}>();".format(name, tsm_type)


def name_timesteppingmethod():
    define_timesteppingmethod("tsm")
    return "tsm"


@class_member(classtag="driver_block")
def typedef_instationarygridoperator(name):
    include_file("dune/pdelab/gridoperator/onestep.hh", filetag="driver_block")
    go_type = type_gridoperator(get_form_ident())
    mass_go_type = type_gridoperator(get_mass_form_ident())
    explicit = get_option('explicit_time_stepping')
    if explicit:
        return "using {} = Dune::PDELab::OneStepGridOperator<{},{},false>;".format(name, go_type, mass_go_type)
    else:
        return "using {} = Dune::PDELab::OneStepGridOperator<{},{}>;".format(name, go_type, mass_go_type)


def type_instationarygridoperator():
    typedef_instationarygridoperator("IGO")
    return "IGO"


@class_member(classtag="driver_block")
def declare_instationarygridoperator(name):
    igo_type = type_instationarygridoperator()
    return "std::shared_ptr<{}> {};".format(igo_type, name)


@preamble(section="gridoperator", kernel="driver_block")
def define_instationarygridoperator(name):
    declare_instationarygridoperator(name)
    igo_type = type_instationarygridoperator()
    go = name_gridoperator(get_form_ident())
    mass_go = name_gridoperator(get_mass_form_ident())
    return "{} = std::make_shared<{}>(*{}, *{});".format(name, igo_type, go, mass_go)


def name_instationarygridoperator():
    define_instationarygridoperator("igo")
    return "igo"


@class_member(classtag="driver_block")
def typedef_onestepmethod(name):
    r_type = type_range()
    igo_type = type_instationarygridoperator()
    snp_type = type_stationarynonlinearproblemssolver(igo_type)
    vector_type = type_vector(get_form_ident())
    return "using {} = Dune::PDELab::OneStepMethod<{}, {}, {}, {}, {}>;".format(name, r_type, igo_type, snp_type, vector_type, vector_type)


def type_onestepmethod():
    typedef_onestepmethod("OSM")
    return "OSM"


@class_member(classtag="driver_block")
def declare_onestepmethod(name):
    ilptype = type_onestepmethod()
    return "std::shared_ptr<{}> {};".format(ilptype, name)


@preamble(section="instat", kernel="driver_block")
def define_onestepmethod(name):
    declare_onestepmethod(name)
    ilptype = type_onestepmethod()
    tsm = name_timesteppingmethod()
    igo_type = type_instationarygridoperator()
    igo = name_instationarygridoperator()
    snp = name_stationarynonlinearproblemsolver(igo_type, igo)
    return "{} = std::make_shared<{}>(*{}, *{}, *{});".format(name, ilptype, tsm, igo, snp)


def name_onestepmethod():
    name = "osm"
    define_onestepmethod(name)
    driver_block_get_onestepmethod(is_implicit=False, name=name)
    return name


@class_member(classtag="driver_block")
def typedef_explicitonestepmethod(name):
    r_type = type_range()
    igo_type = type_instationarygridoperator()
    ls_type = type_linearsolver()
    vector_type = type_vector(get_form_ident())
    return "using {} = Dune::PDELab::ExplicitOneStepMethod<{}, {}, {}, {}>;".format(name, r_type, igo_type, ls_type, vector_type)


def type_explicitonestepmethod():
    typedef_explicitonestepmethod("EOSM")
    return "EOSM"


@class_member(classtag="driver_block")
def declare_explicitonestepmethod(name):
    eosm_type = type_explicitonestepmethod()
    return "std::shared_ptr<{}> {};".format(eosm_type, name)


@preamble(section="instat", kernel="driver_block")
def define_explicitonestepmethod(name):
    declare_explicitonestepmethod(name)
    eosm_type = type_explicitonestepmethod()
    tsm = name_timesteppingmethod()
    igo = name_instationarygridoperator()
    ls = name_linearsolver()
    return "{} = std::make_shared<{}>(*{}, *{}, *{});".format(name, eosm_type, tsm, igo, ls)


def name_explicitonestepmethod():
    name = "eosm"
    define_explicitonestepmethod(name)
    driver_block_get_onestepmethod(is_implicit=False, name=name)
    return name


#
# Export one step method
#


@class_member(classtag="driver_block")
def driver_block_get_onestepmethod(is_implicit=True, name=None):
    if is_implicit:
        if not name:
            name = name_onestepmethod()
        osm_type = type_onestepmethod()

    else:
        if not name:
            name = name_explicitonestepmethod()
        osm_type = type_explicitonestepmethod()
    method_name = "getOneStepMethod"
    return ["std::shared_ptr<{}> {}(){{".format(osm_type, method_name),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_onestepmethod(name, is_implicit=True):
    driver_block_name = name_driver_block()
    driver_block_get_onestepmethod(is_implicit=is_implicit)
    method_name = "getOneStepMethod"
    return "auto {} = {}.{}();".format(name, driver_block_name, method_name)


def main_name_onestepmethod(is_implicit=True):
    name = "oneStepMethod"
    main_define_onestepmethod(name, is_implicit)
    return name
