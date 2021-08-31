"""
The package that provides generating methods for all parts
of the pdelab driver.

Currently, these are hardcoded as strings. It would be possible
to switch these to cgen expression. OTOH, there is not much to be
gained there.

NB: Previously this __init__.py was a module driver.py. As it was growing,
    we made it a package. Some content could and should be separated into
    new modules within this package!
"""
from dune.codegen.error import CodegenCodegenError
from dune.codegen.generation import (generator_factory,
                                     get_global_context_value,
                                     global_context,
                                     include_file,
                                     cached,
                                     pre_include,
                                     preamble,
                                     )
from dune.codegen.options import (get_driverblock_option,
                                  get_form_ident,
                                  get_form_option,
                                  get_option,
                                  )
from ufl import TensorProductCell


#
# The following functions are not doing anything useful, but providing easy access
# to quantities that are needed throughout the process of generating the driver!
#


def get_form(form_ident=None):
    if form_ident is None:
        form_ident = get_form_ident()
    data = get_global_context_value("data")
    return data.object_by_name[get_form_option("form", form_ident)]


def get_dimension():
    return get_form().ufl_cell().geometric_dimension()


def get_cell():
    return get_form().ufl_cell().cellname()


def get_test_element():
    return get_form().arguments()[0].ufl_element()


def get_trial_element():
    return get_form().coefficients()[0].ufl_element()


def is_stationary():
    driver_block = get_option('driver_block_to_build')
    if driver_block is None:
        forms = [i.strip() for i in get_option("operators").split(",")]
        return "mass" not in forms
    else:
        temporal_form = get_driverblock_option("temporal_form")
        return temporal_form is None


def is_linear(form=None):
    '''Test if form is linear in trial function'''
    if form is None:
        form = get_form()
    from ufl import derivative
    from ufl.algorithms import expand_derivatives
    jacform = expand_derivatives(derivative(form, form.coefficients()[0]))
    for coeff in jacform.coefficients():
        if 0 == coeff.count():
            return False

    return True


def isLagrange(fem):
    return fem._short_name in ('CG', 'P', 'Q')


def isSimplical(cell):
    if isinstance(cell, TensorProductCell):
        return False

    # Cells can be identified through strings *or* ufl objects
    if not isinstance(cell, str):
        cell = cell.cellname()
    return cell in ["vertex", "interval", "triangle", "tetrahedron"]


def isQuadrilateral(cell):
    if isinstance(cell, TensorProductCell):
        return all(tuple(isSimplical(c) for c in cell.sub_cells()))

    # Cells can be identified through strings *or* ufl objects
    if not isinstance(cell, str):
        cell = cell.cellname()
    return cell in ["vertex", "interval", "quadrilateral", "hexahedron"]


def isPk(fem):
    return isLagrange(fem) and isSimplical(fem.cell())


def isQk(fem):
    return isLagrange(fem) and isQuadrilateral(fem.cell())


def isDG(fem):
    return fem._short_name is 'DG'


def FEM_name_mangling(fem):
    from ufl import MixedElement, VectorElement, FiniteElement, TensorElement, TensorProductElement
    if isinstance(fem, VectorElement):
        return FEM_name_mangling(fem.sub_elements()[0]) + "_" + str(fem.num_sub_elements())
    if isinstance(fem, TensorElement):
        return FEM_name_mangling(fem.sub_elements()[0]) + "_" + "_".join(str(i) for i in fem.value_shape())
    if isinstance(fem, MixedElement):
        name = ""
        for elem in fem.sub_elements():
            if name is not "":
                name = name + "_"
            name = name + FEM_name_mangling(elem)
        return name
    if isinstance(fem, FiniteElement):
        return "{}{}".format(fem._short_name, fem.degree())
    if isinstance(fem, TensorProductElement):
        assert(len(set(subel._short_name for subel in fem.sub_elements())) == 1)
        return "TP_{}".format("_".join(FEM_name_mangling(subel) for subel in fem.sub_elements()))

    raise NotImplementedError("FEM NAME MANGLING")


def _flatten_list(l):
    if isinstance(l, (tuple, list)):
        for i in l:
            for ni in _flatten_list(i):
                yield ni
    else:
        yield l


def _unroll_list_tensors(expr):
    from ufl.classes import ListTensor
    if isinstance(expr, ListTensor):
        for op in expr.ufl_operands:
            yield op
    else:
        yield expr


def unroll_list_tensors(data):
    for expr in data:
        for e in _unroll_list_tensors(expr):
            yield e


def preprocess_leaf_data(element, data, applyZeroDefault=True):
    data = get_global_context_value("data").object_by_name.get(data, None)
    if data is None and not applyZeroDefault:
        return None

    from ufl import MixedElement
    if isinstance(element, MixedElement):
        # data is None -> use 0 default
        if data is None:
            data = (0,) * element.value_size()

        # Flatten nested lists
        data = tuple(i for i in _flatten_list(data))

        # Expand any list tensors
        data = tuple(i for i in unroll_list_tensors(data))

        assert len(data) == element.value_size()
        return data
    else:
        # Do not return lists for non-MixedElement
        if not isinstance(data, (tuple, list)):
            return (data,)
        else:
            assert len(data) == 1
            return data


def name_inifile():
    # TODO pass some other option here.
    return "argv[1]"


@preamble(section="init", kernel="main")
def parse_initree(varname):
    include_file("dune/common/parametertree.hh", filetag="driver")
    include_file("dune/common/parametertreeparser.hh", filetag="driver")
    filename = name_inifile()
    return ["Dune::ParameterTree initree;", "Dune::ParameterTreeParser::readINITree({}, {});".format(filename, varname)]


def name_initree():
    parse_initree("initree")
    # TODO we can get some other ini file here.
    return "initree"


@preamble(section="init", kernel="main")
def define_mpihelper(name):
    include_file("dune/common/parallel/mpihelper.hh", filetag="driver")
    if get_option("with_mpi"):
        return "Dune::MPIHelper& {} = Dune::MPIHelper::instance(argc, argv);".format(name)
    else:
        return "Dune::FakeMPIHelper& {} = Dune::FakeMPIHelper::instance(argc, argv);".format(name)


def name_mpihelper():
    name = "mpihelper"
    define_mpihelper(name)
    return name


@preamble(section="grid", kernel="main")
def check_parallel_execution():
    from dune.codegen.pdelab.driver.gridfunctionspace import name_leafview
    gv = name_leafview()
    return ["if ({}.comm().size()==1){{".format(gv),
            '  std::cout << "This program should be run in parallel!"  << std::endl;',
            "  return 1;",
            "}"]


def generate_driver_content():
    """Fill cache with driver content"""
    # Make sure that the MPI helper is instantiated
    name_mpihelper()

    # Driver generation entry point
    if get_option("opcounter") or get_option("performance_measuring"):
        if get_option("performance_measuring"):
            assert(not get_option("opcounter"))
        assert(isQuadrilateral(get_cell()))
        # In case of operator counting we only assemble the matrix and evaluate the residual
        # assemble_matrix_timer()
        from dune.codegen.pdelab.driver.timings import apply_jacobian_timer, evaluate_residual_timer
        from dune.codegen.loopy.target import type_floatingpoint
        pre_include("#define HP_TIMER_OPCOUNTER {}".format(type_floatingpoint()), filetag="driver")
        evaluate_residual_timer()
        if get_form_option("generate_jacobian_apply"):
            apply_jacobian_timer()
    elif is_stationary():
        from dune.codegen.pdelab.driver.solve import dune_solve
        vec = dune_solve()
        from dune.codegen.pdelab.driver.vtk import vtkoutput
        vtkoutput()
    else:
        from dune.codegen.pdelab.driver.instationary import solve_instationary
        solve_instationary()

    from dune.codegen.pdelab.driver.error import compare_L2_squared
    if get_option("compare_l2errorsquared"):
        compare_L2_squared()

    # Make sure that timestream is declared before retrieving chache items
    if get_option("instrumentation_level") >= 1:
        from dune.codegen.pdelab.driver.timings import setup_timer
        setup_timer()


def generate_driver():
    # Guarantee that config.h is the very first include in the generated file
    include_file("config.h", filetag="driver")

    # Generate empty driver if there is more than one driverblock
    driverblocks = [i.strip() for i in get_option("driver_blocks").split(",")]
    if len(driverblocks) > 1:
        include_file("iostream", filetag="driver")

        # Include driver block files
        driver_blocks = [i.strip() for i in get_option("driver_blocks").split(",")]
        for db in driver_blocks:
            include_file(get_driverblock_option("filename", db), filetag="driver")

        from cgen import FunctionDeclaration, FunctionBody, Block, Value, LineComment, Line, Generable
        driver_signature = FunctionDeclaration(Value('int', 'main'), [Value('int', 'argc'), Value('char**', 'argv')])
        driver_body = Block([Line("\n"),
                             Line('  std::cout << "This driver is empty" << std::endl;\n'),
                             Line("  return 1;\n"), ])
        driver = FunctionBody(driver_signature, driver_body)

        filename = get_option("driver_file")
        from dune.codegen.file import generate_file
        generate_file(filename, "driver", [driver, ], headerguard=False)

        # Reset the caching data structure
        from dune.codegen.generation import delete_cache_items
        delete_cache_items()

        return

    # Fill cache with driver content
    generate_driver_content()

    # Add check to c++ file if this program should only be used in parallel mode
    if get_option("parallel"):
        check_parallel_execution()

    from dune.codegen.pdelab.driver.error import return_statement
    return_statement()

    from dune.codegen.generation import retrieve_cache_items
    from cgen import FunctionDeclaration, FunctionBody, Block, Value, LineComment, Line, Generable
    driver_signature = FunctionDeclaration(Value('int', 'main'), [Value('int', 'argc'), Value('char**', 'argv')])

    contents = []

    # Assert that this program was called with ini file
    contents += ['if (argc != 2){',
                 '  std::cerr << "This program needs to be called with an ini file" << std::endl;',
                 '  return 1;',
                 '}',
                 '']

    def add_section(tag, comment):
        tagcontents = [i for i in retrieve_cache_items("preamble and main and {}".format(tag), make_generable=True)]
        if tagcontents:
            contents.append(LineComment(comment))
            contents.append(Line("\n"))
            contents.extend(tagcontents)
            contents.append(Line("\n"))

    add_section("init", "Initialize basic stuff...")

    if get_option("instrumentation_level") >= 1:
        init_contents = contents
        contents = []

    add_section("grid", "Setup grid (view)...")
    add_section("driverblock", "Set up driver block...")
    add_section("timings", "Maybe take performance measurements...")
    add_section("solver", "Set up (non)linear solvers...")
    add_section("vtk", "Do visualization...")
    add_section("instat", "Set up instationary stuff...")
    add_section("printing", "Maybe print residuals and matrices to stdout...")
    add_section("error", "Maybe calculate errors for test results...")

    if get_option("instrumentation_level") >= 1:
        from dune.codegen.pdelab.driver.timings import timed_region
        contents = init_contents + timed_region('driver', contents)

    add_section("end", "Stuff that should happen at the end...")
    add_section("return_stmt", "Return statement...")

    contents.insert(0, "\n")
    driver_body = Block([c if isinstance(c, Generable) else Line(c + '\n') for c in contents])

    # Wrap a try/catch block around the driver body
    from dune.codegen.cgen import CatchBlock, TryCatchBlock, Value, Block, Line
    catch_blocks = [CatchBlock(Value("Dune::Exception&", "e"),
                               Block([Line("std::cerr << \"Dune reported error: \" << e << std::endl;\n"),
                                      Line("return 1;\n"),
                                      ])
                               ),
                    CatchBlock(Value("std::exception&", "e"),
                               Block([Line("std::cerr << \"Unknown exception thrown!\" << std::endl;\n"),
                                      Line("return 1;\n"),
                                      ])
                               )
                    ]
    driver_body = Block([TryCatchBlock(driver_body, catch_blocks)])
    driver = FunctionBody(driver_signature, driver_body)

    # Include driver block file
    driver_blocks = [i.strip() for i in get_option("driver_blocks").split(",")]
    assert len(driver_blocks) == 1
    include_file(get_driverblock_option("filename", driver_blocks[0]), filetag="driver")

    # Generate main file
    filename = get_option("driver_file")
    from dune.codegen.file import generate_file
    generate_file(filename, "driver", [driver, ], headerguard=False)

    # Reset the caching data structure
    from dune.codegen.generation import delete_cache_items
    delete_cache_items()


def generate_driver_block(driver_block):
    # Make sure that driver block is initialized
    from dune.codegen.pdelab.driver.driverblock import name_driver_block
    name_driver_block()

    # Fill cache with driver content
    generate_driver_content()

    # Create driver block class from cache
    constructor_preamble_order = ["fem",
                                  "gfs",
                                  "localoperator",
                                  "gridfunction",
                                  "constraints",
                                  "gridoperator",
                                  "vector",
                                  "solver",
                                  "instat"]
    from dune.codegen.pdelab.localoperator import cgen_class_from_cache
    db_class = cgen_class_from_cache("driver_block", constructor_preamble_order=constructor_preamble_order)

    # Create driver block file
    filename = get_driverblock_option("filename")
    from dune.codegen.file import generate_file
    generate_file(filename, "driver_block", [db_class, ], headerguard=True)

    # Reset the caching data structure
    from dune.codegen.generation import delete_cache_items
    delete_cache_items()
