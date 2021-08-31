from dune.codegen.generation import (include_file,
                                     preamble,
                                     )
from dune.codegen.options import get_form_option
from dune.codegen.pdelab.driver import (get_form_ident,
                                        get_trial_element,
                                        name_initree,
                                        )
from dune.codegen.pdelab.driver.gridfunctionspace import (name_leafview,
                                                          main_name_trial_gfs,
                                                          type_leafview,
                                                          )
from dune.codegen.pdelab.driver.solve import main_name_vector


@preamble(section="vtk", kernel="main")
def define_vtkfile(name):
    ini = name_initree()
    include_file("string", filetag="driver")
    return "std::string {} = {}.get<std::string>(\"wrapper.vtkcompare.name\", \"output\");".format(name, ini)


def name_vtkfile():
    define_vtkfile("vtkfile")
    return "vtkfile"


@preamble(section="vtk", kernel="main")
def typedef_vtkwriter(name):
    include_file("dune/grid/io/file/vtk/subsamplingvtkwriter.hh", filetag="driver")
    gv = type_leafview()
    return "using {} = Dune::SubsamplingVTKWriter<{}>;".format(name, gv)


def type_vtkwriter():
    typedef_vtkwriter("VTKWriter")
    return "VTKWriter"


@preamble(section="vtk", kernel="main")
def define_subsamplinglevel(name):
    ini = name_initree()
    degree = get_trial_element().degree()
    if isinstance(degree, tuple):
        degree = max(degree)
    if get_form_option("blockstructured"):
        degree *= get_form_option("number_of_blocks")
    return "Dune::RefinementIntervals {}({}.get<int>(\"vtk.subsamplinglevel\", {}));".format(name, ini, max(degree, 1))


def name_subsamplingintervals():
    define_subsamplinglevel("subint")
    return "subint"


@preamble(section="vtk", kernel="main")
def define_vtkwriter(name):
    _type = type_vtkwriter()
    gv = name_leafview()
    subsamp = name_subsamplingintervals()
    return "{} {}({}, {});".format(_type, name, gv, subsamp)


def name_vtkwriter():
    define_vtkwriter("vtkwriter")
    return "vtkwriter"


@preamble(section="vtk", kernel="main")
def vtkoutput():
    include_file("dune/pdelab/gridfunctionspace/vtk.hh", filetag="driver")
    vtkwriter = name_vtkwriter()
    gfs = main_name_trial_gfs()
    vtkfile = name_vtkfile()
    predicate = name_predicate()
    vec = main_name_vector(get_form_ident())

    return ["Dune::PDELab::addSolutionToVTKWriter({}, *{}, *{}, Dune::PDELab::vtk::defaultNameScheme(), {});".format(vtkwriter, gfs, vec, predicate),
            "{}.write({}, Dune::VTK::ascii);".format(vtkwriter, vtkfile)]


def type_predicate():
    include_file("dune/codegen/vtkpredicate.hh", filetag="driver")
    return "CuttingPredicate"


@preamble(section="vtk", kernel="main")
def define_predicate(name):
    t = type_predicate()
    return "{} {};".format(t, name)


def name_predicate():
    define_predicate("predicate")
    return "predicate"


@preamble(section="vtk", kernel="main")
def typedef_vtk_sequence_writer(name):
    include_file("dune/grid/io/file/vtk/vtksequencewriter.hh", filetag="driver")
    gv_type = type_leafview()
    return "using {} = Dune::VTKSequenceWriter<{}>;".format(name, gv_type)


def type_vtk_sequence_writer():
    typedef_vtk_sequence_writer("VTKSW")
    return "VTKSW"


@preamble(section="vtk", kernel="main")
def define_vtk_sequence_writer(name):
    vtksw_type = type_vtk_sequence_writer()
    vtkw_type = type_vtkwriter()
    vtkw = name_vtkwriter()
    vtkfile = name_vtkfile()
    return "{} {}(std::make_shared<{}>({}), {});".format(vtksw_type, name, vtkw_type, vtkw, vtkfile)


def name_vtk_sequence_writer():
    define_vtk_sequence_writer("vtkSequenceWriter")
    return "vtkSequenceWriter"


@preamble(section="vtk", kernel="main")
def visualize_initial_condition():
    include_file("dune/pdelab/gridfunctionspace/vtk.hh", filetag="driver")
    vtkwriter = name_vtk_sequence_writer()
    element = get_trial_element()
    gfs = main_name_trial_gfs()
    vector = main_name_vector(get_form_ident())
    predicate = name_predicate()
    from dune.codegen.pdelab.driver.instationary import name_time
    time = name_time()
    return ["Dune::PDELab::addSolutionToVTKWriter({}, *{}, *{}, Dune::PDELab::vtk::defaultNameScheme(), {});".format(vtkwriter, gfs, vector, predicate),
            "{}.write({}, Dune::VTK::appendedraw);".format(vtkwriter, time)]
