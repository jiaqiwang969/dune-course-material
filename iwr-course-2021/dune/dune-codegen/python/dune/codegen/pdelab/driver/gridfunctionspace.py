from dune.codegen.error import CodegenUnsupportedFiniteElementError
from dune.codegen.generation import (class_basename,
                                     class_member,
                                     include_file,
                                     preamble,
                                     )
from dune.codegen.options import (get_form_option,
                                  get_option,
                                  )
from dune.codegen.pdelab.driver import (FEM_name_mangling,
                                        get_cell,
                                        get_dimension,
                                        get_test_element,
                                        get_trial_element,
                                        isQuadrilateral,
                                        isSimplical,
                                        name_initree,
                                        preprocess_leaf_data,
                                        )
from dune.codegen.pdelab.driver.driverblock import (grid_function_identifier,
                                                    name_driver_block,
                                                    type_driver_block,)
from dune.codegen.loopy.target import type_floatingpoint

from ufl import FiniteElement, MixedElement, TensorElement, VectorElement, TensorProductElement, TensorProductCell


@class_member(classtag="driver_block")
def typedef_domainfield(name):
    gridt = type_leafview()
    return "using {} = typename {}::ctype;".format(name, gridt)


def type_domainfield():
    typedef_domainfield("DF")
    return "DF"


@class_member(classtag="driver_block")
def typedef_range(name):
    return "using {} = {};".format(name, type_floatingpoint())


def type_range():
    name = "RangeType"
    typedef_range(name)
    return name


@preamble(section="init", kernel="main")
def main_typedef_range(name):
    return "using {} = {};".format(name, type_floatingpoint())


def main_type_range():
    name = "RangeType"
    main_typedef_range(name)
    return name


@preamble(section="grid", kernel="main")
def typedef_grid(name):
    dim = get_dimension()
    if isQuadrilateral(get_trial_element().cell()):
        range_type = main_type_range()
        if get_option("grid_unstructured"):
            gridt = "Dune::UGGrid<{}>".format(dim)
            include_file("dune/grid/uggrid.hh", filetag="driver")
        elif get_option("yaspgrid_offset"):
            gridt = "Dune::YaspGrid<{0}, Dune::EquidistantOffsetCoordinates<{1}, {0}>>".format(dim, range_type)
        else:
            gridt = "Dune::YaspGrid<{0}, Dune::EquidistantCoordinates<{1}, {0}>>".format(dim, range_type)
        include_file("dune/grid/yaspgrid.hh", filetag="driver")
    else:
        if isSimplical(get_trial_element().cell()):
            # gridt = "Dune::UGGrid<{}>".format(dim)
            # include_file("dune/grid/uggrid.hh", filetag="driver")
            gridt = "Dune::ALUGrid<{}, {}, Dune::simplex, Dune::conforming>".format(dim, dim)
            include_file("dune/alugrid/grid.hh", filetag="driver")
        else:
            raise CodegenCodegenError("Cant match your geometry with a DUNE grid. Please report bug.")
    return "using {} = {};".format(name, gridt)


def type_grid():
    name = "Grid"
    typedef_grid(name)
    return name


@preamble(section="grid", kernel="main")
def define_grid(name):
    include_file("dune/testtools/gridconstruction.hh", filetag="driver")
    ini = name_initree()
    _type = type_grid()
    # TODO: In principle this is only necessary if we use sum factorization in
    # one of the operators. So this could be turned off if that is not the case.
    if isQuadrilateral(get_trial_element().cell()) and get_option("grid_unstructured") and not \
            get_option("grid_consistent"):
        include_file("dune/consistent-edge-orientation/createconsistentgrid.hh", filetag="driver")
        return ["IniGridFactory<{}> factory({});".format(_type, ini),
                "std::shared_ptr<{}> grid_nonconsistent = factory.getGrid();".format(_type),
                "std::shared_ptr<{}> grid = createConsistentGrid(grid_nonconsistent);".format(_type)]
    return ["IniGridFactory<{}> factory({});".format(_type, ini),
            "std::shared_ptr<{}> grid = factory.getGrid();".format(_type)]


def name_grid():
    name = "grid"
    define_grid(name)
    return name


@preamble(section="grid", kernel="main")
def typedef_leafview(name):
    grid = type_grid()
    return "using {} = {}::LeafGridView;".format(name, grid)


def type_leafview():
    name = "GV"
    typedef_leafview(name)
    return name


@preamble(section="grid", kernel="main")
def define_leafview(name):
    _type = type_leafview()
    grid = name_grid()
    return "{} {} = {}->leafGridView();".format(_type, name, grid)


def name_leafview():
    name = "gv"
    define_leafview(name)
    return name


def get_short_name(element):
    if isinstance(element, TensorProductElement):
        assert len(set(subel._short_name for subel in element.sub_elements())) == 1
        return get_short_name(element.sub_elements()[0])

    return element._short_name


@class_member(classtag="driver_block")
def typedef_fem(element, name):
    gv = type_leafview()
    df = type_domainfield()
    r = type_range()
    dim = get_dimension()
    cell = element.cell()
    degree = element.degree()
    short = get_short_name(element)

    # We currently only support TensorProductElement from UFL if it aliases another finite element
    # available from UFL. Here, we check this condition and recover the aliases element
    if isinstance(element, TensorProductElement):
        subels = set(subel._short_name for subel in element.sub_elements())
        if len(subels) != 1 or len(set(element.degree())) != 1:
            raise CodegenUnsupportedFiniteElementError(element)

        degree = element.degree()[0]
        cell = TensorProductCell(*tuple(subel.cell() for subel in element.sub_elements()))

    # The blockstructured code branch has its own handling of finite element selection
    if get_form_option("blockstructured"):
        include_file("dune/codegen/blockstructured/blockstructuredqkfem.hh", filetag="driver_block")
        degree = degree * get_form_option("number_of_blocks")
        return "using {} = Dune::PDELab::BlockstructuredQkLocalFiniteElementMap<{}, {}, {}, {}>;" \
            .format(name, gv, df, r, degree)

    # This is a backward-compatibility hack: So far we silently used OPBFem for DG with simplices:
    if short == "DG" and isSimplical(cell):
        short = "OPB"

    # Choose the correct finite element implementation
    if short == "CG":
        if isSimplical(cell):
            if dim in (1, 2, 3):
                include_file("dune/pdelab/finiteelementmap/pkfem.hh", filetag="driver_block")
                return "using {} = Dune::PDELab::PkLocalFiniteElementMap<{}, {}, {}, {}>;" \
                    .format(name, gv, df, r, degree)
            else:
                raise CodegenUnsupportedFiniteElementError(element)
        elif isQuadrilateral(cell):
            if dim in (2, 3) and degree < 3:
                include_file("dune/pdelab/finiteelementmap/qkfem.hh", filetag="driver_block")
                return "using {} = Dune::PDELab::QkLocalFiniteElementMap<{}, {}, {}, {}>;" \
                    .format(name, gv, df, r, degree)
            else:
                raise CodegenUnsupportedFiniteElementError(element)
        else:
            raise CodegenUnsupportedFiniteElementError(element)
    elif short == "DG":
        if isQuadrilateral(cell):
            if dim < 4:
                include_file("dune/pdelab/finiteelementmap/qkdg.hh", filetag="driver_block")
                return "using {} = Dune::PDELab::QkDGLocalFiniteElementMap<{}, {}, {}, {}>;" \
                    .format(name, df, r, degree, dim)
            else:
                raise CodegenUnsupportedFiniteElementError(element)
        else:
            raise CodegenUnsupportedFiniteElementError(element)
    elif short == "GL":
        raise NotImplementedError("Gauss-Legendre polynomials not implemented")
    elif short == "DGLL":
        raise NotImplementedError("Discontinuous Gauss-Lobatto-Legendre polynomials not implemented")
    elif short == "OPB":
        if isQuadrilateral(cell):
            gt = "Dune::GeometryType::cube"
        elif isSimplical(cell):
            gt = "Dune::GeometryType::simplex"
        else:
            raise CodegenUnsupportedFiniteElementError(element)

        include_file("dune/pdelab/finiteelementmap/opbfem.hh", filetag="driver_block")
        return "using {} = Dune::PDELab::OPBLocalFiniteElementMap<{}, {}, {}, {}, {}>;" \
            .format(name, df, r, degree, dim, gt)
    elif short == "Monom":
        raise NotImplementedError("Monomials basis DG not implemented")
    elif short == "RaTu":
        raise NotImplementedError("Rannacher-Turek elements not implemented")
    elif short == "RT":
        raise NotImplementedError("Raviart-Thomas elements not implemented")
    elif short == "BDM":
        raise NotImplementedError("Brezzi-Douglas-Marini elements not implemented")
    else:
        raise CodegenUnsupportedFiniteElementError(element)


def type_fem(element):
    name = "{}_FEM".format(FEM_name_mangling(element).upper())
    typedef_fem(element, name)
    return name


@class_member(classtag="driver_block")
def declare_fem(element, name):
    fem_type = type_fem(element)
    return "std::shared_ptr<{}> {};".format(fem_type, name)


@preamble(section="fem", kernel="driver_block")
def define_fem(element, name):
    declare_fem(element, name)
    femtype = type_fem(element)

    # Determine whether the FEM is grid-dependent - currently on the Lagrange elements are
    if get_short_name(element) == "CG":
        gv = name_leafview()
        return "{} =  std::make_shared<{}>({});".format(name, femtype, gv)
    else:
        return "{} = std::make_shared<{}>();".format(name, femtype)


def name_fem(element):
    assert isinstance(element, (FiniteElement, TensorProductElement))
    name = "{}_fem".format(FEM_name_mangling(element).lower())
    define_fem(element, name)
    return name


def name_trial_gfs():
    element = get_trial_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    return name_gfs(element, is_dirichlet)


def main_name_trial_gfs():
    name = "gridFunctionSpace"
    element = get_trial_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    main_define_gfs(name, element, is_dirichlet)
    return name


def name_test_gfs():
    element = get_test_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    return name_gfs(element, is_dirichlet)


def name_gfs(element, is_dirichlet, treepath=(), root=True):
    """Generate name of grid function space

    This function will call itself recursively to build the grid function space
    tree.

    Parameters
    ----------
    element : UFL FiniteElement
    is_dirichlet : Tuple
        Which parts of the treepath use dirichlet constraints?
    treepath :
        Treepath for the grid function space tree
    root : bool
        Called for the root of the tree?
    """
    if isinstance(element, (VectorElement, TensorElement)):
        subel = element.sub_elements()[0]
        subgfs = name_gfs(subel, is_dirichlet[:subel.value_size()], treepath=treepath + (0,), root=False)
        name = "{}_pow{}gfs_{}".format(subgfs,
                                       element.num_sub_elements(),
                                       "_".join(str(t) for t in treepath))
        define_power_gfs(element, is_dirichlet, name, subgfs, root)
    elif isinstance(element, MixedElement):
        k = 0
        subgfs = []
        for i, subel in enumerate(element.sub_elements()):
            subgfs.append(name_gfs(subel, is_dirichlet[k:k + subel.value_size()], treepath=treepath + (i,), root=False))
            k = k + subel.value_size()
        name = "_".join(subgfs)
        if len(subgfs) == 1:
            name = "{}_dummy".format(name)
        name = "{}_{}".format(name, "_".join(str(t) for t in treepath))
        define_composite_gfs(element, is_dirichlet, name, tuple(subgfs), root)
    else:
        assert isinstance(element, (FiniteElement, TensorProductElement))
        name = "{}{}_gfs_{}".format(FEM_name_mangling(element).lower(),
                                    "_dirichlet" if is_dirichlet[0] else "",
                                    "_".join(str(t) for t in treepath))

        define_gfs(element, is_dirichlet, name, root)

    if root:
        driver_block_get_gridfunctionsspace(element, is_dirichlet, name=name)

    return name


def type_test_gfs():
    element = get_test_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    return type_gfs(element, is_dirichlet)


def type_trial_gfs():
    element = get_trial_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    return type_gfs(element, is_dirichlet)


def type_gfs(element, is_dirichlet, root=True):
    if isinstance(element, (VectorElement, TensorElement)):
        subel = element.sub_elements()[0]
        subgfs = type_gfs(subel, is_dirichlet[:subel.value_size()], root=False)
        name = "{}_POW{}GFS".format(subgfs, element.num_sub_elements())
        typedef_power_gfs(element, is_dirichlet, name, subgfs, root)
        return name
    elif isinstance(element, MixedElement):
        k = 0
        subgfs = []
        for subel in element.sub_elements():
            subgfs.append(type_gfs(subel, is_dirichlet[k:k + subel.value_size()], root=False))
            k = k + subel.value_size()
        name = "_".join(subgfs)
        if len(subgfs) == 1:
            name = "{}_dummy".format(name)
        typedef_composite_gfs(element, name, tuple(subgfs), root)
        return name
    else:
        assert isinstance(element, (FiniteElement, TensorProductElement))
        name = "{}{}_GFS".format(FEM_name_mangling(element).upper(),
                                 "_dirichlet" if is_dirichlet[0] else "",
                                 )
        typedef_gfs(element, is_dirichlet, name, root)
        return name


@class_member(classtag="driver_block")
def declare_gfs(element, is_dirichlet, name, root):
    gfstype = type_gfs(element, is_dirichlet, root=root)
    return "std::shared_ptr<{}> {};".format(gfstype, name)


@preamble(section="gfs", kernel="driver_block")
def define_gfs(element, is_dirichlet, name, root):
    declare_gfs(element, is_dirichlet, name, root)
    gfstype = type_gfs(element, is_dirichlet, root=root)
    gv = name_leafview()
    fem = name_fem(element)
    return ["{} = std::make_shared<{}>({}, *{});".format(name, gfstype, gv, fem),
            "{}->name(\"{}\");".format(name, name)]


@preamble(section="gfs", kernel="driver_block")
def define_power_gfs(element, is_dirichlet, name, subgfs, root):
    declare_gfs(element, is_dirichlet, name, root)
    gfstype = type_gfs(element, is_dirichlet, root=root)
    names = ["using namespace Dune::Indices;"]
    names = names + ["{0}->child(_{1}).name(\"{0}_{1}\");".format(name, i) for i in range(element.num_sub_elements())]
    return ["{} = std::make_shared<{}>(*{});".format(name, gfstype, subgfs)] + names


@preamble(section="gfs", kernel="driver_block")
def define_composite_gfs(element, is_dirichlet, name, subgfs, root):
    declare_gfs(element, is_dirichlet, name, root)
    gfstype = type_gfs(element, is_dirichlet, root=root)
    return ["{} = std::make_shared<{}>({});".format(name, gfstype, ", ".join("*{}".format(c) for c in subgfs)),
            "{}->update();".format(name)]


@class_member(classtag="driver_block")
def typedef_gfs(element, is_dirichlet, name, root):
    vb = type_vectorbackend(element, root)
    gv = type_leafview()
    fem = type_fem(element)
    from dune.codegen.pdelab.driver.constraints import has_dirichlet_constraints
    cass = type_constraintsassembler(has_dirichlet_constraints(is_dirichlet))
    return "using {} = Dune::PDELab::GridFunctionSpace<{}, {}, {}, {}>;".format(name, gv, fem, cass, vb)


@class_member(classtag="driver_block")
def typedef_power_gfs(element, is_dirichlet, name, subgfs, root):
    include_file("dune/pdelab/gridfunctionspace/powergridfunctionspace.hh", filetag="driver_block")
    vb = type_vectorbackend(element, root)
    ot = type_orderingtag(False)

    return "using {} = Dune::PDELab::PowerGridFunctionSpace<{}, {}, {}, {}>;".format(name, subgfs, element.num_sub_elements(), vb, ot)


@class_member(classtag="driver_block")
def typedef_composite_gfs(element, name, subgfs, root):
    vb = type_vectorbackend(element, root)
    ot = type_orderingtag(isinstance(element, FiniteElement))
    args = ", ".join(subgfs)
    return "using {} = Dune::PDELab::CompositeGridFunctionSpace<{}, {}, {}>;".format(name, vb, ot, args)


@class_member(classtag="driver_block")
def typedef_vectorbackend(name, element, root):
    include_file("dune/pdelab/backend/istl.hh", filetag="driver_block")
    if get_form_option("fastdg") and root:
        blocking = "Dune::PDELab::ISTL::Blocking::fixed"
        if isinstance(element, MixedElement):
            blocksize = ""
        else:
            include_file("dune/pdelab/finiteelement/qkdglagrange.hh", filetag="driver_block")
            blocksize = ", Dune::QkStuff::QkSize<{}, {}>::value".format(element.degree(), get_dimension())
    else:
        blocking = "Dune::PDELab::ISTL::Blocking::none"
        blocksize = ""

    return "using {} = Dune::PDELab::ISTL::VectorBackend<{}{}>;".format(name, blocking, blocksize)


def type_vectorbackend(element, root):
    name = "VectorBackend{}".format(FEM_name_mangling(element).upper())
    typedef_vectorbackend(name, element, root)
    return name


def type_orderingtag(leaf):
    if leaf or not get_form_option("fastdg"):
        return "Dune::PDELab::LexicographicOrderingTag"
    else:
        return "Dune::PDELab::EntityBlockedOrderingTag"


@class_member(classtag="driver_block")
def typedef_overlapping_dirichlet_constraintsassembler(name):
    include_file("dune/pdelab/constraints/conforming.hh", filetag="driver_block")
    return "using {} = Dune::PDELab::ConformingDirichletConstraints;".format(name)


@class_member(classtag="driver_block")
def typedef_p0parallel_constraintsassembler(name):
    include_file("dune/pdelab/constraints/p0.hh", filetag="driver_block")
    return "using {} = Dune::PDELab::P0ParallelConstraints;".format(name)


@class_member(classtag="driver_block")
def typedef_dirichlet_constraintsassembler(name):
    include_file("dune/pdelab/constraints/conforming.hh", filetag="driver_block")
    return "using {} = Dune::PDELab::ConformingDirichletConstraints;".format(name)


@class_member(classtag="driver_block")
def typedef_no_constraintsassembler(name):
    return "using {} = Dune::PDELab::NoConstraints;".format(name)


def type_constraintsassembler(is_dirichlet):
    assert isinstance(is_dirichlet, bool)
    overlapping = get_option("overlapping")
    if is_dirichlet and not overlapping:
        name = "DirichletConstraintsAssember"
        typedef_dirichlet_constraintsassembler(name)
    elif is_dirichlet and overlapping:
        name = "OverlappingConformingDirichletConstraints"
        typedef_overlapping_dirichlet_constraintsassembler(name)
    elif not is_dirichlet and overlapping:
        name = "P0ParallelConstraints"
        typedef_p0parallel_constraintsassembler(name)
    else:
        assert not is_dirichlet and not overlapping
        name = "NoConstraintsAssembler"
        typedef_no_constraintsassembler(name)
    return name


def main_type_subgfs(treepath):
    include_file('dune/pdelab/gridfunctionspace/subspace.hh', filetag='driver')
    gfs = main_type_trial_gfs()
    indices = ", ".join("Dune::index_constant<{}>".format(t) for t in treepath)
    return "Dune::PDELab::GridFunctionSubSpace<{}, Dune::TypeTree::HybridTreePath<{}> >".format(gfs, indices)


@preamble(section="driverblock", kernel="main")
def main_define_subgfs(name, treepath):
    t = main_type_subgfs(treepath)
    gfs = main_name_trial_gfs()
    return "{} {}(*{});".format(t, name, gfs)


def main_name_subgfs(treepath):
    gfs = main_name_trial_gfs()
    name = "{}_{}".format(gfs, "_".join(str(t) for t in treepath))
    main_define_subgfs(name, treepath)
    return name


def main_name_trial_subgfs(treepath):
    if len(treepath) == 0:
        return main_name_trial_gfs()
    else:
        return main_name_subgfs(treepath)


@class_member(classtag="driver_block")
def driver_block_get_gridfunctionsspace(element, is_dirichlet, name=None):
    gfs_type = type_gfs(element, is_dirichlet)
    if not name:
        name = name_gfs(element, is_dirichlet)
    return ["std::shared_ptr<{}> getGridFunctionsSpace(){{".format(gfs_type),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_typedef_trial_gfs(name, element, is_dirichlet):
    driver_block_type = type_driver_block()
    db_gfs_type = type_gfs(element, is_dirichlet)
    return "using {} = {}::{};".format(name, driver_block_type, db_gfs_type)


def main_type_trial_gfs():
    name = "GridFunctionSpace"
    element = get_trial_element()
    identifier = "is_dirichlet"
    is_dirichlet = preprocess_leaf_data(element, grid_function_identifier(identifier))
    main_typedef_trial_gfs(name, element, is_dirichlet)
    return name


@preamble(section="driverblock", kernel="main")
def main_define_gfs(name, element, is_dirichlet):
    driver_block_name = name_driver_block()
    driver_block_get_gridfunctionsspace(element, is_dirichlet)
    return "auto {} = {}.getGridFunctionsSpace();".format(name, driver_block_name)
