from dune.codegen.generation import (class_member,
                                     get_global_context_value,
                                     include_file,
                                     preamble,
                                     )
from dune.codegen.pdelab.driver import (get_form_ident,
                                        get_cell,
                                        get_dimension,
                                        get_test_element,
                                        get_trial_element,
                                        isQuadrilateral,
                                        name_initree,
                                        )
from dune.codegen.pdelab.driver.constraints import (name_assembled_constraints,
                                                    type_constraintscontainer,
                                                    )
from dune.codegen.pdelab.driver.driverblock import (name_driver_block,
                                                    type_driver_block,
                                                    )
from dune.codegen.pdelab.driver.gridfunctionspace import (name_gfs,
                                                          name_test_gfs,
                                                          name_trial_gfs,
                                                          type_domainfield,
                                                          type_gfs,
                                                          type_range,
                                                          type_test_gfs,
                                                          type_trial_gfs,
                                                          )
from dune.codegen.pdelab.localoperator import localoperator_basename
from dune.codegen.options import (get_form_option,
                                  get_mass_form_ident,
                                  )

from ufl import FiniteElement, VectorElement


@class_member(classtag="driver_block")
def typedef_gridoperator(name, form_ident):
    ugfs = type_trial_gfs()
    vgfs = type_test_gfs()
    lop = type_localoperator(form_ident)
    cc = type_constraintscontainer()
    mb = type_matrixbackend()
    df = type_domainfield()
    r = type_range()
    if get_form_option("fastdg"):
        if not get_form_option("sumfact"):
            raise CodegenCodegenError("FastDGGridOperator is only implemented for sumfactorization.")
        include_file("dune/pdelab/gridoperator/fastdg.hh", filetag="driver_block")
        return "using {} = Dune::PDELab::FastDGGridOperator<{}, {}, {}, {}, {}, {}, {}, {}, {}>;".format(name, ugfs, vgfs, lop, mb, df, r, r, cc, cc)
    else:
        include_file("dune/pdelab/gridoperator/gridoperator.hh", filetag="driver_block")
        return "using {} = Dune::PDELab::GridOperator<{}, {}, {}, {}, {}, {}, {}, {}, {}>;".format(name, ugfs, vgfs, lop, mb, df, r, r, cc, cc)


def type_gridoperator(form_ident):
    name = "GO_{}".format(form_ident)
    typedef_gridoperator(name, form_ident)
    return name


@class_member(classtag="driver_block")
def declare_gridoperator(name, form_ident):
    gotype = type_gridoperator(form_ident)
    return "std::shared_ptr<{}> {};".format(gotype, name)


@preamble(section="gridoperator", kernel="driver_block")
def define_gridoperator(name, form_ident):
    declare_gridoperator(name, form_ident)
    gotype = type_gridoperator(form_ident)
    ugfs = name_trial_gfs()
    vgfs = name_test_gfs()
    if ugfs != vgfs:
        raise NotImplementedError("Non-Galerkin methods currently not supported!")
    cc = name_assembled_constraints()
    lop = name_localoperator(form_ident)
    mb = name_matrixbackend()
    return ["{} = std::make_shared<{}>(*{}, *{}, *{}, *{}, *{}, *{});".format(name, gotype, ugfs, cc, vgfs, cc, lop, mb),
            "std::cout << \"gfs with \" << {}->size() << \" dofs generated  \"<< std::endl;".format(ugfs),
            "std::cout << \"cc with \" << {}->size() << \" dofs generated  \"<< std::endl;".format(cc)]


def name_gridoperator(form_ident):
    name = "go_{}".format(form_ident)
    define_gridoperator(name, form_ident)
    driver_block_get_gridoperator(form_ident, name=name)
    return name


@preamble(section="driverblock", kernel="main")
def main_typedef_gridoperator(name, form_ident):
    driver_block_type = type_driver_block()
    db_gridoperator_type = type_gridoperator(form_ident)
    gridoperator_type = "using {} = {}::{};".format(name, driver_block_type, db_gridoperator_type)
    return gridoperator_type


def main_type_gridoperator(form_ident):
    name = "GridOperator"
    main_typedef_gridoperator(name, form_ident)
    return name


@class_member(classtag="driver_block")
def driver_block_get_gridoperator(form_ident, name=None):
    gridoperator_type = type_gridoperator(form_ident)
    if not name:
        name = name_gridoperator(form_ident)

    if form_ident == get_mass_form_ident():
        return ["std::shared_ptr<{}> getMassGridOperator(){{".format(gridoperator_type),
                "  return {};".format(name),
                "}"]

    return ["std::shared_ptr<{}> getGridOperator(){{".format(gridoperator_type),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_gridoperator(name, form_ident):
    driver_block_name = name_driver_block()
    driver_block_get_gridoperator(form_ident)
    return "auto {} = {}.getGridOperator();".format(name, driver_block_name)


def main_name_gridoperator(form_ident):
    name = "gridOperator"
    main_define_gridoperator(name, form_ident)
    return name


@class_member(classtag="driver_block")
def typedef_localoperator(name, form_ident):
    ugfs = type_trial_gfs()
    vgfs = type_test_gfs()
    filename = get_form_option("filename", form_ident)
    include_file(filename, filetag="driver_block")
    lopname = localoperator_basename(form_ident)

    from dune.codegen.pdelab.driver import get_form
    form = get_form(form_ident)
    coefficients = sorted(filter(lambda c: c.count() > 2, form.coefficients()), key=lambda c: c.count())
    if len(coefficients) == 0:
        return "using {} = {}<{}, {}>;".format(name, lopname, ugfs, vgfs)
    else:
        coefficient_gfss = []
        for c in coefficients:
            coefficient_gfss.append(type_coefficient_gfs(c))
        return "using {} = {}<{}, {}, {}>;".format(name, lopname, ugfs, vgfs, ",".join(coefficient_gfss))


def type_localoperator(form_ident):
    name = "LOP_{}".format(form_ident.upper())
    typedef_localoperator(name, form_ident)
    return name


@class_member(classtag="driver_block")
def declare_localoperator(name, form_ident):
    loptype = type_localoperator(form_ident)
    return "std::shared_ptr<{}> {};".format(loptype, name)


@preamble(section="localoperator", kernel="driver_block")
def define_localoperator(name, form_ident):
    # The localoperator might depend on additional finite element functions. In
    # this case we need to generate dicsrete grid view functions
    generate_localoperator_coefficient_functions(name, form_ident)

    declare_localoperator(name, form_ident)
    trial_gfs = name_trial_gfs()
    test_gfs = name_test_gfs()
    loptype = type_localoperator(form_ident)
    ini = name_initree()
    return "{} = std::make_shared<{}>(*{}, *{}, {});".format(name, loptype, trial_gfs, test_gfs, ini)


def name_localoperator(form_ident):
    name = "lop_{}".format(form_ident)
    define_localoperator(name, form_ident)
    driver_block_get_localoperator(form_ident, name=name)
    return name


@class_member(classtag="driver_block")
def driver_block_get_localoperator(form_ident, name=None):
    if not name:
        name = name_localoperator(form_ident)
    localoperator_type = type_localoperator(form_ident)
    method_name = "getLocalOperator"
    if form_ident == get_mass_form_ident():
        method_name = "getLocalMassOperator"
    return ["std::shared_ptr<{}> {}(){{".format(localoperator_type, method_name),
            "  return {};".format(name),
            "}"]


@preamble(section="driverblock", kernel="main")
def main_define_localoperator(name, form_ident):
    driver_block_name = name_driver_block()
    driver_block_get_localoperator(form_ident)
    method_name = "getLocalOperator"
    if form_ident == "mass":
        method_name = "getLocalMassOperator"
    return "auto {} = {}.{}();".format(name, driver_block_name, method_name)


def main_name_localoperator(form_ident):
    name = "localOperator{}".format(form_ident.capitalize())
    main_define_localoperator(name, form_ident)
    return name


def generate_localoperator_coefficient_functions(lop_name, form_ident):
    from dune.codegen.pdelab.driver import get_form
    form = get_form(form_ident)
    coefficients = sorted(filter(lambda c: c.count() > 2, form.coefficients()), key=lambda c: c.count())
    for c in coefficients:
        driver_block_set_coefficient_function(lop_name, c)


@class_member(classtag="driver_block")
def driver_block_set_coefficient_function(lop_name, coefficient):
    coeff_gridfunctionspace = name_coefficient_gfs(coefficient)
    coeff_gridfunctionspace_type = type_coefficient_gfs(coefficient)
    coeff_vector = name_coefficient_vector(coefficient)
    coeff_vector_type = type_coefficient_vector(coefficient)

    method_name = "setCoefficient{}".format(_cf_ident(coefficient))
    return ["void {}(std::shared_ptr<{}> p_gfs, std::shared_ptr<{}> p_z){{".format(method_name,
                                                                                   coeff_gridfunctionspace_type,
                                                                                   coeff_vector_type),
            "  {} = p_gfs;".format(coeff_gridfunctionspace),
            "  {} = p_z;".format(coeff_vector),
            "  {}->{}({}, {});".format(lop_name, method_name, coeff_gridfunctionspace, coeff_vector),
            "}"]


def _cf_ident(coefficient):
    name = coefficient.codegen_cargo("name")
    if name is None:
        name = str(coefficient.count() - 2)
    return name


@class_member(classtag="driver_block")
def typedef_coefficient_vector(name, coefficient):
    element = coefficient.ufl_element()

    # The type of the GridFunctionSpace depends on the constraints. When the
    # form depends on non ansatz coefficients we need to pass this information
    # along. We pass this along through the codegen_cargo() method on the
    # coeffiecient.
    is_dirichlet = coefficient.codegen_cargo("is_dirichlet")

    # Note: root=False makes sure that no driver_block_get_... method is called
    gfs_type = type_gfs(element, is_dirichlet, root=False)
    df = type_domainfield()
    return "using {} = Dune::PDELab::Backend::Vector<{}, {}>;".format(name, gfs_type, df)


def type_coefficient_vector(coefficient):
    name = "CoefficientVector{}".format(_cf_ident(coefficient))
    typedef_coefficient_vector(name, coefficient)
    return name


@class_member(classtag="driver_block")
def declare_coefficient_vector(name, coefficient):
    cv_type = type_coefficient_vector(coefficient)
    return "std::shared_ptr<{}> {};".format(cv_type, name)


def name_coefficient_vector(coefficient):
    name = "coefficientVector{}".format(_cf_ident(coefficient))
    declare_coefficient_vector(name, coefficient)
    return name


@class_member(classtag="driver_block")
def driver_block_typedef_gfs(name, coefficient):
    element = coefficient.ufl_element()

    # The type of the GridFunctionSpace depends on the constraints. When the
    # form depends on non ansatz coefficients we need to pass this information
    # along. We pass this along through the codegen_cargo() method on the
    # coeffiecient.
    is_dirichlet = coefficient.codegen_cargo("is_dirichlet")

    # Note: root=False makes sure that no driver_block_get_... method is called
    gfs_type = type_gfs(element, is_dirichlet, root=False)
    return "using {} = {};".format(name, gfs_type)


def type_coefficient_gfs(coefficient):
    name = "CoefficientGridFunctionSpace{}".format(_cf_ident(coefficient))
    driver_block_typedef_gfs(name, coefficient)
    return name


@class_member(classtag="driver_block")
def declare_coefficient_gfs(name, coefficient):
    gfs_type = type_coefficient_gfs(coefficient)
    return "std::shared_ptr<{}> {};".format(gfs_type, name)


def name_coefficient_gfs(coefficient):
    name = "coefficientGridFunctionSpace{}".format(_cf_ident(coefficient))
    declare_coefficient_gfs(name, coefficient)
    return name


@preamble(section="gridoperator", kernel="driver_block")
def define_dofestimate(name):
    # Provide a worstcase estimate for the number of entries per row based
    # on the given gridfunction space and cell geometry
    if isQuadrilateral(get_cell()):
        geo_factor = 2**get_dimension()
    else:
        if get_dimension() < 3:
            geo_factor = 3 * get_dimension()
        else:
            # TODO no idea how a generic estimate for 3D simplices looks like
            geo_factor = 12

    gfs = name_trial_gfs()
    ini = name_initree()

    return ["{}->update();".format(gfs),
            "int generic_dof_estimate =  {} * {}->maxLocalSize();".format(geo_factor, gfs),
            "int {} = {}.get<int>(\"istl.number_of_nnz\", generic_dof_estimate);".format(name, ini)]


def name_dofestimate():
    name = "dofestimate"
    define_dofestimate(name)
    return name


@class_member(classtag="driver_block")
def typedef_matrixbackend(name):
    include_file("dune/pdelab/backend/istl.hh", filetag="driver_block")
    return "using {} = Dune::PDELab::ISTL::BCRSMatrixBackend<>;".format(name)


def type_matrixbackend():
    name = "MatrixBackend"
    typedef_matrixbackend(name)
    return name


@class_member(classtag="driver_block")
def declare_matrixbackend(name):
    mbtype = type_matrixbackend()
    return "std::shared_ptr<{}> {};".format(mbtype, name)


@preamble(section="gridoperator", kernel="driver_block")
def define_matrixbackend(name):
    declare_matrixbackend(name)
    mbtype = type_matrixbackend()
    dof = name_dofestimate()
    return "{} = std::make_shared<{}>({});".format(name, mbtype, dof)


def name_matrixbackend():
    name = "mb"
    define_matrixbackend(name)
    return name
