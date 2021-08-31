""" Timing related generator functions """

from dune.codegen.generation import (cached,
                                     include_file,
                                     pre_include,
                                     preamble,
                                     post_include)
from dune.codegen.options import (get_option,
                                  get_form_ident,
                                  )
from dune.codegen.pdelab.driver import (get_form_ident,
                                        is_linear,
                                        name_initree,
                                        name_mpihelper,
                                        )
from dune.codegen.pdelab.driver.gridfunctionspace import (main_name_trial_gfs,
                                                          name_leafview,
                                                          type_leafview,
                                                          )
from dune.codegen.pdelab.driver.gridoperator import (main_name_gridoperator,
                                                     main_name_localoperator,
                                                     main_type_gridoperator,
                                                     )
from dune.codegen.pdelab.driver.solve import (main_name_vector,
                                              main_type_vector,
                                              )


_sde_marks = {}


@preamble(section="timings", kernel="main")
def define_timing_identifier(name):
    ini = name_initree()
    return "auto {} = {}.get<std::string>(\"identifier\", std::string(argv[0]));".format(name, ini)


def name_timing_identifier():
    name = "ident"
    define_timing_identifier(name)
    return name


@preamble(section="timings", kernel="main")
def dump_dof_numbers(stream):
    ident = name_timing_identifier()
    level = get_option("instrumentation_level")
    include_file("dune/pdelab/common/partitionviewentityset.hh", filetag="driver")
    gvt = type_leafview()
    gv = name_leafview()

    from dune.codegen.pdelab.driver import get_trial_element, isDG, _flatten_list
    from ufl import MixedElement, TensorProductElement
    element = get_trial_element()

    def _apply_to_element(element, f):
        if isinstance(element, MixedElement) or isinstance(element, TensorProductElement):
            return tuple(_apply_to_element(e, f) for e in element.sub_elements())
        else:
            return f(element)
    element_is_dg = all(_flatten_list(_apply_to_element(element, isDG)))

    if element_is_dg:
        return ["Dune::PDELab::NonOverlappingEntitySet<{}> es({});".format(gvt, gv),
                "{} << \"{} \" << {} << \" dofs dofs \" << {}->maxLocalSize() * es.size(0) << std::endl;".format(stream,
                                                                                                                 level,
                                                                                                                 ident,
                                                                                                                 main_name_trial_gfs())
                ]
    else:
        return ["{} << \"{} \" << {} << \" dofs dofs \" << {}->size() << std::endl;".format(stream, level, ident,
                                                                                            main_name_trial_gfs())
                ]


@preamble(section="timings", kernel="main")
def define_timing_stream(name):
    include_file('fstream', filetag='driver', system=True)
    include_file('sstream', filetag='driver', system=True)
    include_file('sys/types.h', filetag='driver', system=True)
    include_file('chrono', filetag='driver', system=True)

    return ["std::stringstream ss;",
            "ss << \"{}/timings-rank-\" << {}.rank() << \"-\" << std::chrono::high_resolution_clock::now().time_since_epoch().count() << \".csv\";".format(get_option('project_basedir'), name_mpihelper()),
            "std::ofstream {};".format(name),
            "{}.open(ss.str(), std::ios_base::app);".format(name),
            ]


def name_timing_stream():
    name = "timestream"
    define_timing_stream(name)
    dump_dof_numbers(name)
    return name


@preamble(section="timings", kernel="main")
def define_temporary_vector(name, form_ident):
    vector_type = main_type_vector(form_ident)
    gfs = main_name_trial_gfs()
    return ["{} {}(*{});".format(vector_type, name, gfs), "{} = 0.0;".format(name)]


def name_temporary_vector(name, form):
    name = "{}_{}".format(name, form)
    define_temporary_vector(name, form)
    return name


@preamble(section="timings", kernel="main")
def define_jacobian(name, form_ident):
    t_go = main_type_gridoperator(form_ident)
    n_go = main_name_gridoperator(form_ident)
    return ["using M_{} = typename {}::Traits::Jacobian;".format(form_ident, t_go),
            "M_{} {}(*{});".format(form_ident, name, n_go)]


def name_jacobian(form_ident):
    name = "J_{}".format(form_ident)
    define_jacobian(name, form_ident)
    return name


@preamble(section="init", kernel="main")
def init_likwid():
    return ["LIKWID_MARKER_INIT;", "LIKWID_MARKER_THREADINIT;"]


@preamble(section="end", kernel="main")
def finalize_likwid():
    return ["LIKWID_MARKER_CLOSE;"]


@preamble(section="timings", kernel="main")
def local_operator_likwid():
    lop_name = main_name_localoperator(get_form_ident())
    return "{}->register_likwid_timers();".format(lop_name)


@preamble(section="timings", kernel="main")
def local_operator_ssc_marks():
    lop_name = main_name_localoperator(get_form_ident())
    return "{}->dump_ssc_marks();".format(lop_name)


def ssc_macro():
    return '#define __SSC_MARK(x) do{ __asm__ __volatile__' \
           '("movl %0, %%ebx; .byte 100, 103, 144" : :"i"(x) : "%ebx"); } while(0)'


@cached
def setup_timer():
    # TODO check that we are using YASP?
    if get_option("use_likwid"):
        pre_include("#define LIKWID_PERFMON", filetag="driver")
        include_file("likwid.h", filetag="driver")
        init_likwid()
        if get_option('instrumentation_level') >= 3:
            import logging
            logger = logging.getLogger(__name__)
            logger.warning("timings: using instrumentation level >= 3 with likwid will slow down your code considerably")
            local_operator_likwid()
        finalize_likwid()
    elif get_option("use_sde"):
        post_include(ssc_macro(), filetag='driver')
        if get_option('instrumentation_level') >= 3:
            local_operator_ssc_marks()
    else:
        from dune.codegen.loopy.target import type_floatingpoint
        pre_include("#define HP_TIMER_OPCOUNTER {}".format(type_floatingpoint()), filetag="driver")
        if get_option('opcounter'):
            pre_include("#define ENABLE_COUNTER", filetag="driver")
        pre_include("#define ENABLE_HP_TIMERS", filetag="driver")
        include_file("dune/codegen/common/timer.hh", filetag="driver")


@preamble(section="init", kernel="main")
def init_likwid_timer(region):
    return ["LIKWID_MARKER_REGISTER(\"{}\");".format(region)]


def init_region_timer(region):
    setup_timer()
    if get_option("use_likwid"):
        init_likwid_timer(region)
    elif get_option("use_sde"):
        pass
    else:
        from dune.codegen.generation import post_include
        post_include("HP_DECLARE_TIMER({});".format(region), filetag="driver")


def get_region_marks(region, driver):
    if driver:
        return _sde_marks.setdefault(region, (2 * (len(_sde_marks) + 1) * 11, (2 * (len(_sde_marks) + 1) + 1) * 11))
    else:
        return _sde_marks.setdefault(region, (2 * (len(_sde_marks) + 1) * 1, (2 * (len(_sde_marks) + 1) + 1) * 1))


def start_region_timer(region):
    if get_option("use_likwid"):
        return ["LIKWID_MARKER_START(\"{}\");".format(region)]
    elif get_option("use_sde"):
        marks = get_region_marks(region, driver=True)
        return ["__SSC_MARK(0x{});".format(marks[0])]
    else:
        return ["HP_TIMER_START({});".format(region)]


def stop_region_timer(region):
    if get_option("use_likwid"):
        return ["LIKWID_MARKER_STOP(\"{}\");".format(region)]
    elif get_option("use_sde"):
        marks = get_region_marks(region, driver=True)
        return ["__SSC_MARK(0x{});".format(marks[1]),
                "std::cout << \"Timed region {}: {} <--> {}\" << std::endl;".format(region, *marks)]
    else:
        timestream = name_timing_stream()
        return ["HP_TIMER_STOP({});".format(region),
                "DUMP_TIMER({}, {}, {}, true);".format(get_option("instrumentation_level"), region, timestream)]


def start_region_timer_instruction(region, **kwargs):
    if get_option("use_likwid"):
        code = "LIKWID_MARKER_START(\"{}\");".format(region)
    else:
        code = "HP_TIMER_START({});".format(region)
    from loopy import CInstruction
    return CInstruction([], code, **kwargs)


def stop_region_timer_instruction(region, **kwargs):
    if get_option("use_likwid"):
        code = "LIKWID_MARKER_STOP(\"{}\");".format(region)
    else:
        code = "HP_TIMER_STOP({});".format(region)
    from loopy import CInstruction
    return CInstruction([], code, **kwargs)


def timed_region(region, actions):
    if isinstance(actions, str):
        actions = [actions]

    assert(isinstance(actions, list))

    if get_option('instrumentation_level') >= 2:
        assembly = []
        print_times = []

        init_region_timer(region)

        if get_option('instrumentation_level') >= 3 and not (get_option('use_likwid') or get_option("use_sde")):
            timestream = name_timing_stream()
            lop_name = main_name_localoperator(get_form_ident())
            print_times.append("{}->dump_timers({}, {}, true);".format(lop_name, timestream, name_timing_identifier()))

        assembly += start_region_timer(region)
        assembly += actions
        assembly += stop_region_timer(region)

        return assembly + print_times
    else:
        return actions


@preamble(section="timings", kernel="main")
def evaluate_residual_timer():
    n_go = main_name_gridoperator(get_form_ident())
    v = main_name_vector(get_form_ident())
    r = name_temporary_vector("r", get_form_ident())

    action = "{}->residual(*{}, {});".format(n_go, v, r)

    return timed_region("residual_evaluation", action)


@preamble(section="timings", kernel="main")
def apply_jacobian_timer():
    form = get_form_ident()
    n_go = main_name_gridoperator(form)
    v = main_name_vector(form)

    if is_linear():
        j = name_temporary_vector("j", form)
        action = "{}->jacobian_apply(*{}, {});".format(n_go, v, j)
    else:
        j0 = name_temporary_vector("j0", form)
        j1 = name_temporary_vector("j1", form)
        action = "{}->nonlinear_jacobian_apply(*{}, {}, {});".format(n_go, v, j0, j1)

    return timed_region("apply_jacobian", action)


@preamble(section="timings", kernel="main")
def assemble_matrix_timer():
    n_go = main_name_gridoperator(get_form_ident())
    v = main_name_vector(get_form_ident())
    m = name_jacobian(get_form_ident())

    action = "{}->jacobian(*{},{});".format(n_go, v, m)

    return timed_region("matrix_assembly", action)
