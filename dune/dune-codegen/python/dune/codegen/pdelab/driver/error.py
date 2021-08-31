""" Generator functions to calculate errors in the driver """

from dune.codegen.generation import (cached,
                                     include_file,
                                     preamble,
                                     )
from dune.codegen.options import get_option
from dune.codegen.pdelab.driver import (get_form_ident,
                                        get_trial_element,
                                        )
from dune.codegen.pdelab.driver.gridfunctionspace import (main_type_trial_gfs,
                                                          name_leafview,
                                                          main_name_trial_subgfs,
                                                          main_type_range,
                                                          main_type_subgfs,
                                                          )
from dune.codegen.pdelab.driver.interpolate import (main_name_grid_function,
                                                    main_type_grid_function,
                                                    )
from dune.codegen.pdelab.driver.solve import (define_vector,
                                              dune_solve,
                                              main_name_vector,
                                              main_type_vector,
                                              )
from ufl import MixedElement, TensorElement, VectorElement


@preamble(section="error", kernel="main")
def define_test_fail_variable(name):
    return 'bool {}(false);'.format(name)


def name_test_fail_variable():
    name = "testfail"
    define_test_fail_variable(name)
    return name


def type_discrete_grid_function(treepath):
    name = "DiscreteGridFunction_{}".format("_".join(str(t) for t in treepath))
    return name


@preamble(section="error", kernel="main")
def define_discrete_grid_function(gfs, vector_name, dgf_name, treepath):
    dgf_type = type_discrete_grid_function(treepath)
    if len(treepath) == 0:
        gfs_type = main_type_trial_gfs()
    else:
        gfs_type = main_type_subgfs(treepath)
    form_ident = get_form_ident()
    vector_type = main_type_vector(form_ident)

    # If this is the root we get the gfs from the driver block as a
    # pointer. This means we need to dereference it
    if len(treepath) == 0:
        gfs = '*' + gfs
    return ["using {} = Dune::PDELab::DiscreteGridFunction<{}, {}>;".format(dgf_type, gfs_type, vector_type),
            "{} {}({}, *{});".format(dgf_type, dgf_name, gfs, vector_name)]


def name_discrete_grid_function(gfs, vector_name, treepath):
    name = "discreteGridFunction_{}".format("_".join(str(t) for t in treepath))
    define_discrete_grid_function(gfs, vector_name, name, treepath)
    return name


@preamble(section="error", kernel="main")
def typedef_difference_squared_adapter(name, treepath):
    bgf_type = main_type_grid_function("exact_solution", treepath)

    # Discrete grid function (numerical solution)
    gfs = main_name_trial_subgfs(treepath)
    vector = main_name_vector(get_form_ident())
    dgf = name_discrete_grid_function(gfs, vector, treepath)
    dgf_type = type_discrete_grid_function(treepath)

    return 'using {} = Dune::PDELab::DifferenceSquaredAdapter<{}, {}>;'.format(name, bgf_type, dgf_type)


def type_difference_squared_adapter(treepath):
    name = 'DifferenceSquaredAdapter_{}'.format("_".join(str(t) for t in treepath))
    typedef_difference_squared_adapter(name, treepath)
    return name


@preamble(section="error", kernel="main")
def define_difference_squared_adapter(name, treepath):
    t = type_difference_squared_adapter(treepath)
    sol = main_name_grid_function("exact_solution", treepath)
    if len(treepath) == 0:
        sol = "*{}".format(sol)
    vector = main_name_vector(get_form_ident())
    gfs = main_name_trial_subgfs(treepath)
    dgf = name_discrete_grid_function(gfs, vector, treepath)

    return '{} {}({}, {});'.format(t, name, sol, dgf)


def name_difference_squared_adapter(treepath):
    name = 'dsa_{}'.format("_".join(str(t) for t in treepath))
    define_difference_squared_adapter(name, treepath)
    return name


@preamble(section="error", kernel="main")
def _accumulate_L2_squared(treepath):
    dsa = name_difference_squared_adapter(treepath)
    accum_error = name_accumulated_L2_error()

    include_file("dune/pdelab/gridfunctionspace/gridfunctionadapter.hh", filetag="driver")
    include_file("dune/pdelab/common/functionutilities.hh", filetag="driver")

    strtp = ", ".join(str(t) for t in treepath)

    gv = name_leafview()
    sum_error_over_ranks = ""
    if get_option("parallel"):
        sum_error_over_ranks = "  err = {}.comm().sum(err);".format(gv)
    return ["{",
            "  // L2 error squared of difference between numerical",
            "  // solution and the interpolation of exact solution",
            "  // for treepath ({})".format(strtp),
            "  typename decltype({})::Traits::RangeType err(0.0);".format(dsa),
            "  Dune::PDELab::integrateGridFunction({}, err, 10);".format(dsa),
            sum_error_over_ranks,
            "  {} += err;".format(accum_error),
            "  if ({}.comm().rank() == 0){{".format(gv),
            "    std::cout << \"L2 Error for treepath {}: \" << err << std::endl;".format(strtp),
            "  }"
            "}",
            ]


def get_treepath(element, index):
    if isinstance(element, (VectorElement, TensorElement)):
        return (index,)
    if isinstance(element, MixedElement):
        pos, rest = element.extract_subelement_component(index)
        offset = sum(element.sub_elements()[i].value_size() for i in range(pos))
        return (pos,) + get_treepath(element.sub_elements()[pos], index - offset)
    else:
        return ()


def treepath_to_index(element, treepath, offset=0):
    if len(treepath) == 0:
        return offset
    index = treepath[0]
    offset = offset + sum(element.sub_elements()[i].value_size() for i in range(index))
    subel = element.sub_elements()[index]
    return treepath_to_index(subel, treepath[1:], offset)


def accumulate_L2_squared():
    element = get_trial_element()
    if isinstance(element, MixedElement):
        tree_pathes = (True,) * element.value_size()
        if get_option("l2error_tree_path") is not None:
            tree_pathes = list(map(int, get_option("l2error_tree_path").split(',')))
            assert len(tree_pathes) == element.value_size()
        for i, path in enumerate(tree_pathes):
            if path:
                _accumulate_L2_squared(get_treepath(element, i))
    else:
        _accumulate_L2_squared(())


@preamble(section="error", kernel="main")
def define_accumulated_L2_error(name):
    t = main_type_range()
    return "Dune::FieldVector<{}, 1> {}(0.0);".format(t, name)


def name_accumulated_L2_error():
    name = 'l2error'
    define_accumulated_L2_error(name)
    return name


@preamble(section="error", kernel="main")
def compare_L2_squared():
    accumulate_L2_squared()
    gv = name_leafview()

    accum_error = name_accumulated_L2_error()
    fail = name_test_fail_variable()
    return ["using std::abs;",
            "using std::isnan;",
            "if ({}.comm().rank() == 0){{".format(gv),
            "  std::cout << \"\\nl2errorsquared: \" << {} << std::endl << std::endl;".format(accum_error),
            "}",
            "if (isnan({0}[0]) or abs({0}[0])>{1})".format(accum_error, get_option("compare_l2errorsquared")),
            "  {} = true;".format(fail)]


@preamble(section="return_stmt", kernel="main")
def return_statement():
    fail = name_test_fail_variable()
    return "return {};".format(fail)
