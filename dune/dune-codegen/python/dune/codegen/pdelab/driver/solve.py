from dune.codegen.generation import (class_basename,
                                     class_member,
                                     constructor_parameter,
                                     include_file,
                                     initializer_list,
                                     preamble,
                                     template_parameter
                                     )
from dune.codegen.options import (get_form_option,
                                  get_option,
                                  )
from dune.codegen.pdelab.driver import (get_form_ident,
                                        is_linear,
                                        is_stationary,
                                        name_initree,
                                        )
from dune.codegen.pdelab.driver.driverblock import (name_driver_block,
                                                    type_driver_block,
                                                    )
from dune.codegen.pdelab.driver.gridfunctionspace import (main_name_trial_gfs,
                                                          name_trial_gfs,
                                                          name_leafview,
                                                          type_domainfield,
                                                          type_leafview,
                                                          type_trial_gfs,
                                                          )
from dune.codegen.pdelab.driver.constraints import (type_constraintscontainer,
                                                    name_assembled_constraints,
                                                    )
from dune.codegen.pdelab.driver.gridoperator import (main_name_gridoperator,
                                                     main_type_gridoperator,
                                                     name_gridoperator,
                                                     type_gridoperator,
                                                     )
from dune.codegen.pdelab.driver.interpolate import interpolate_dirichlet_data
from dune.codegen.pdelab.geometry import world_dimension


@preamble(section="solver", kernel="main")
def dune_solve():
    form_ident = get_form_ident()

    # Test if form is linear in ansatzfunction
    linear = is_linear()

    # Test wether we want to do matrix free operator evaluation
    matrix_free = get_form_option('matrix_free')
    # Get right solve command
    if linear and matrix_free:
        go = main_name_gridoperator(form_ident)
        x = main_name_vector(form_ident)
        include_file("dune/codegen/matrixfree.hh", filetag="driver")
        solve = "solveMatrixFree(*{},*{});".format(go, x)
    elif linear and not matrix_free:
        slp = main_name_stationarylinearproblemsolver()
        solve = "{}->apply();".format(slp)
    elif not linear and matrix_free:
        # TODO copy of linear case and obviously broken, used to generate something ;)
        go = main_name_gridoperator(form_ident)
        x = main_name_vector(form_ident)
        include_file("dune/codegen/matrixfree.hh", filetag="driver")
        solve = "solveNonlinearMatrixFree(*{},*{});".format(go, x)
    elif not linear and not matrix_free:
        go_type = main_type_gridoperator(form_ident)
        go = main_name_gridoperator(form_ident)
        snp = main_name_stationarynonlinearproblemsolver()
        solve = "{}->apply();".format(snp)

    if get_form_option("generate_residuals"):
        print_residual()
    if get_form_option("generate_jacobians"):
        print_matrix()

    from dune.codegen.pdelab.driver.timings import timed_region
    solve = timed_region('solve', solve)

    return solve


@class_member(classtag="driver_block")
def typedef_vector(name, form_ident):
    gfs = type_trial_gfs()
    df = type_domainfield()
    return "using {} = Dune::PDELab::Backend::Vector<{},{}>;".format(name, gfs, df)


def type_vector(form_ident):
    name = "V_{}".format(form_ident.upper())
    typedef_vector(name, form_ident)
    return name


@class_member(classtag="driver_block")
def declare_vector(name, form_ident):
    vtype = type_vector(form_ident)
    return "std::shared_ptr<{}> {};".format(vtype, name)


@preamble(section="vector", kernel="driver_block")
def define_vector(name, form_ident):
    declare_vector(name, form_ident)
    vtype = type_vector(form_ident)
    gfs = name_trial_gfs()
    return ["{} = std::make_shared<{}>(*{});".format(name, vtype, gfs), "*{} = 0.0;".format(name)]


def name_vector(form_ident):
    name = "x_{}".format(form_ident)
    define_vector(name, form_ident)

    # Register get method
    driver_block_get_coefficient(form_ident, name=name)

    # Interpolate dirichlet boundary condition
    interpolate_dirichlet_data(name)
    return name


@preamble(section="driverblock", kernel="main")
def main_typedef_vector(name, form_ident):
    driver_block_type = type_driver_block()
    db_vector_type = type_vector(form_ident)
    vector_type = "using {} = {}::{};".format(name, driver_block_type, db_vector_type)
    return vector_type


def main_type_vector(form_ident):
    name = "Coefficient"
    main_typedef_vector(name, form_ident)
    return name


@class_member(classtag="driver_block")
def driver_block_get_coefficient(form_ident, name=None):
    vector_type = type_vector(form_ident)
    if not name:
        name = name_vector(form_ident)
    return ["std::shared_ptr<{}> getCoefficient(){{".format(vector_type),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_vector(name, form_ident):
    driver_block_name = name_driver_block()
    driver_block_get_coefficient(form_ident)
    return "auto {} = {}.getCoefficient();".format(name, driver_block_name)


def main_name_vector(form_ident):
    name = "coefficient"
    main_define_vector(name, form_ident)
    return name


@class_member(classtag="driver_block")
def typedef_linearsolver(name):
    include_file("dune/pdelab/backend/istl.hh", filetag="driver_block")
    if get_option('overlapping'):
        gfs = type_trial_gfs()
        cc = type_constraintscontainer()
        return "using {} = Dune::PDELab::ISTLBackend_OVLP_BCGS_ILU0<{},{}>;".format(name, gfs, cc)
    else:
        return "using {} = Dune::PDELab::ISTLBackend_SEQ_SuperLU;".format(name)


def type_linearsolver():
    name = "LinearSolver"
    typedef_linearsolver(name)
    return name


@class_member(classtag="driver_block")
def declare_linearsolver(name):
    lstype = type_linearsolver()
    return "std::shared_ptr<{}> {};".format(lstype, name)


@preamble(section="solver", kernel="driver_block")
def define_linearsolver(name):
    declare_linearsolver(name)
    lstype = type_linearsolver()
    if get_option('overlapping'):
        gfs = name_trial_gfs()
        cc = name_assembled_constraints()
        return "{} = std::make_shared<{}>(*{}, *{});".format(name, lstype, gfs, cc)
    else:
        return "{} = std::make_shared<{}>(false);".format(name, lstype)


def name_linearsolver():
    name = "ls"
    define_linearsolver(name)
    return name


@preamble(section="solver", kernel="driver_block")
def define_reduction(name):
    ini = name_initree()
    return "double {} = {}.get<double>(\"reduction\", 1e-12);".format(name, ini)


def name_reduction():
    name = "reduction"
    define_reduction(name)
    return name


@class_member(classtag="driver_block")
def typedef_stationarylinearproblemsolver(name):
    include_file("dune/pdelab/stationary/linearproblem.hh", filetag="driver_block")
    gotype = type_gridoperator(get_form_ident())
    lstype = type_linearsolver()
    xtype = type_vector(get_form_ident())
    return "using {} = Dune::PDELab::StationaryLinearProblemSolver<{}, {}, {}>;".format(name, gotype, lstype, xtype)


def type_stationarylinearproblemsolver():
    typedef_stationarylinearproblemsolver("SLP")
    return "SLP"


@class_member(classtag="driver_block")
def declare_stationarylinearproblemsolver(name):
    slptype = type_stationarylinearproblemsolver()
    return "std::shared_ptr<{}> {};".format(slptype, name)


@preamble(section="solver", kernel="driver_block")
def define_stationarylinearproblemsolver(name):
    declare_stationarylinearproblemsolver(name)
    slptype = type_stationarylinearproblemsolver()
    go = name_gridoperator(get_form_ident())
    ls = name_linearsolver()
    x = name_vector(get_form_ident())
    red = name_reduction()
    return "{} = std::make_shared<{}>(*{}, *{}, *{}, {});".format(name, slptype, go, ls, x, red)


def name_stationarylinearproblemsolver():
    name = "slp"
    define_stationarylinearproblemsolver(name)
    driver_block_get_solver(name=name)
    return name


@class_member(classtag="driver_block")
def driver_block_get_solver(name=None):
    solver_type = type_stationarylinearproblemsolver()
    if not name:
        name = name_stationarylinearproblemsolver()
    return ["std::shared_ptr<{}> getSolver(){{".format(solver_type),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_stationarylinearproblemsolver(name):
    driver_block_name = name_driver_block()
    driver_block_get_solver()
    return "auto {} = {}.getSolver();".format(name, driver_block_name)


def main_name_stationarylinearproblemsolver():
    name = "solver"
    main_define_stationarylinearproblemsolver(name)
    return name


@class_member(classtag="driver_block")
def typedef_stationarynonlinearproblemsolver(name, go_type):
    include_file("dune/pdelab/newton/newton.hh", filetag="driver_block")
    ls_type = type_linearsolver()
    x_type = type_vector(get_form_ident())
    return "using {} = Dune::PDELab::Newton<{}, {}, {}>;".format(name, go_type, ls_type, x_type)


def type_stationarynonlinearproblemssolver(go_type):
    name = "SNP"
    typedef_stationarynonlinearproblemsolver(name, go_type)
    return name


@class_member(classtag="driver_block")
def declare_stationarynonlinearproblemsolver(name, go_type):
    snp_type = type_stationarynonlinearproblemssolver(go_type)
    return "std::shared_ptr<{}> {};".format(snp_type, name)


@preamble(section="solver", kernel="driver_block")
def define_stationarynonlinearproblemsolver(name, go_type, go):
    declare_stationarynonlinearproblemsolver(name, go_type)
    snp_type = type_stationarynonlinearproblemssolver(go_type)
    x = name_vector(get_form_ident())
    ls = name_linearsolver()
    return "{} = std::make_shared<{}>(*{}, *{}, *{});".format(name, snp_type, go, x, ls)


def name_stationarynonlinearproblemsolver(go_type, go):
    name = "snp"
    define_stationarynonlinearproblemsolver(name, go_type, go)
    driver_block_get_nonlinear_solver(name=name)
    return name


@class_member(classtag="driver_block")
def driver_block_get_nonlinear_solver(name=None):
    go = name_gridoperator(get_form_ident())
    if is_stationary():
        go_type = type_gridoperator(get_form_ident())
    else:
        from dune.codegen.pdelab.driver.instationary import type_instationarygridoperator
        go_type = type_instationarygridoperator()
    if not name:
        name = name_stationarynonlinearproblemsolver(go_type, go)
    solver_type = type_stationarynonlinearproblemssolver(go_type)
    return ["std::shared_ptr<{}> getSolver(){{".format(solver_type),
            "  return {};".format(name),
            "}"]


@preamble(section="solver", kernel="main")
def main_define_stationarynonlinearproblemsolver(name):
    driver_block_name = name_driver_block()
    driver_block_get_nonlinear_solver()
    return "auto {} = {}.getSolver();".format(name, driver_block_name)


def main_name_stationarynonlinearproblemsolver():
    name = "solver"
    main_define_stationarynonlinearproblemsolver(name)
    return name


def random_input(v):
    include_file("random", system=True, filetag="driver")
    return ["  // Setup random input",
            "  std::size_t seed = 0;",
            "  auto rng = std::mt19937_64(seed);",
            "  auto dist = std::uniform_real_distribution<>(-1., 1.);",
            "  for (auto& v : *{})".format(v),
            "    v = dist(rng);"]


def interpolate_input(v):
    dim = world_dimension()
    gv = name_leafview()
    gfs = main_name_trial_gfs()
    expr = []
    for i in range(dim):
        expr.append("x[{}]*x[{}]".format(i, i))
    expr = "+".join(expr)
    return ["  // Interpolate input",
            "  auto interpolate_lambda = [] (const auto& x){",
            "    return std::exp({});".format(expr),
            "  };",
            "  auto interpolate = Dune::PDELab::makeGridFunctionFromCallable({}, interpolate_lambda);".format(gv),
            "  Dune::PDELab::interpolate(interpolate, *{}, *{});".format(gfs, v),
            ]


@preamble(section="printing", kernel="main")
def print_residual():
    ini = name_initree()
    n_go = main_name_gridoperator(get_form_ident())
    v = main_name_vector(get_form_ident())
    t_v = main_type_vector(get_form_ident())

    if get_option("debug_interpolate_input"):
        input = interpolate_input(v)
    else:
        input = random_input(v)

    return ["if ({}.get<bool>(\"printresidual\", false)) {{".format(ini),
            "  using Dune::PDELab::Backend::native;",
            "  {} r(*{});".format(t_v, v)] + input + \
           ["  r=0.0;",
            "  {}->residual(*{}, r);".format(n_go, v),
            "  Dune::printvector(std::cout, native(r), \"residual vector\", \"row\");",
            "}"]


@preamble(section="printing", kernel="main")
def print_matrix():
    ini = name_initree()
    t_go = main_type_gridoperator(get_form_ident())
    n_go = main_name_gridoperator(get_form_ident())
    v = main_name_vector(get_form_ident())
    t_v = main_type_vector(get_form_ident())

    if get_option("debug_interpolate_input"):
        input = interpolate_input(v)
    else:
        input = random_input(v)

    return ["if ({}.get<bool>(\"printmatrix\", false)) {{".format(ini),
            "  using Dune::PDELab::Backend::native;",
            "  {} r(*{});".format(t_v, v)] + input + \
           ["  using M = typename {}::Traits::Jacobian;".format(t_go),
            "  M m(*{});".format(n_go),
            "  {}->jacobian(*{},m);".format(n_go, v),
            "  using Dune::PDELab::Backend::native;",
            "  Dune::printmatrix(std::cout, native(m),\"global stiffness matrix\",\"row\",9,1);",
            "}"]
