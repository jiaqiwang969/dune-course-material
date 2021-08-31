#ifndef POISSON_MC_DRIVER_HH
#define POISSON_MC_DRIVER_HH


#include "dune/pdelab/gridfunctionspace/vtk.hh"
#include "dune/pdelab/backend/istl.hh"
#include "dune/common/parametertreeparser.hh"
#include "dune/pdelab/stationary/linearproblem.hh"
#include "dune/testtools/gridconstruction.hh"
#include <random>
#include "dune/pdelab/function/callableadapter.hh"
#include "dune/alugrid/grid.hh"
#include "string"
#include "dune/codegen/vtkpredicate.hh"
#include "dune/pdelab/gridfunctionspace/gridfunctionadapter.hh"
#include "dune/common/parametertree.hh"
#include "dune/pdelab/gridoperator/gridoperator.hh"
#include "dune/grid/io/file/vtk/subsamplingvtkwriter.hh"
#include "dune/pdelab/common/functionutilities.hh"
#include "dune/pdelab/finiteelementmap/pkfem.hh"
#include "dune/pdelab/constraints/conforming.hh"
#include "dune/pdelab/function/discretegridviewfunction.hh"

#include "poisson_mc_operator_r.hh"
#include "poisson_mc_operator_r_adjoint.hh"
#include "poisson_mc_operator_r_control.hh"


bool driver(int argc, char** argv){
  // Initialize basic stuff...
  using RangeType = double;
  Dune::ParameterTree initree;
  Dune::ParameterTreeParser::readINITree(argv[1], initree);

  // Setup grid (view)...
  using Grid = Dune::ALUGrid<2, 2, Dune::simplex, Dune::conforming>;
  using GV = Grid::LeafGridView;
  using DF = Grid::ctype;
  IniGridFactory<Grid> factory(initree);
  std::shared_ptr<Grid> grid = factory.getGrid();
  GV gv = grid->leafGridView();

  // Set up finite element maps...
  using P1_FEM = Dune::PDELab::PkLocalFiniteElementMap<GV, DF, RangeType, 1>;
  P1_FEM p1_fem(gv);

  // Set up grid function spaces...
  using VectorBackendP1 = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::none>;
  using DirichletConstraintsAssember = Dune::PDELab::ConformingDirichletConstraints;
  using P1_dirichlet_GFS = Dune::PDELab::GridFunctionSpace<GV, P1_FEM, DirichletConstraintsAssember, VectorBackendP1>;
  P1_dirichlet_GFS p1_dirichlet_gfs_(gv, p1_fem);
  p1_dirichlet_gfs_.name("p1_dirichlet_gfs_");

  // Set up constraints container...
  using P1_dirichlet_GFS_CC = P1_dirichlet_GFS::ConstraintsContainer<RangeType>::Type;
  P1_dirichlet_GFS_CC p1_dirichlet_gfs__cc;
  p1_dirichlet_gfs__cc.clear();
  auto p1_bctype_lambda = [&](const auto& x){ return 1.0; };
  auto p1_bctype = Dune::PDELab::makeBoundaryConditionFromCallable(gv, p1_bctype_lambda);
  Dune::PDELab::constraints(p1_bctype, p1_dirichlet_gfs_, p1_dirichlet_gfs__cc);

  // Set up grid grid operators...
  using LOP_R = ROperator<P1_dirichlet_GFS, P1_dirichlet_GFS>;
  using MatrixBackend = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
  using GO_r = Dune::PDELab::GridOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, LOP_R, MatrixBackend, DF, RangeType, RangeType, P1_dirichlet_GFS_CC, P1_dirichlet_GFS_CC>;
  LOP_R lop_r(p1_dirichlet_gfs_, p1_dirichlet_gfs_, initree);
  p1_dirichlet_gfs_.update();
  int generic_dof_estimate =  6 * p1_dirichlet_gfs_.maxLocalSize();
  int dofestimate = initree.get<int>("istl.number_of_nnz", generic_dof_estimate);
  MatrixBackend mb(dofestimate);
  GO_r go_r(p1_dirichlet_gfs_, p1_dirichlet_gfs__cc, p1_dirichlet_gfs_, p1_dirichlet_gfs__cc, lop_r, mb);
  std::cout << "gfs with " << p1_dirichlet_gfs_.size() << " dofs generated  "<< std::endl;
  std::cout << "cc with " << p1_dirichlet_gfs__cc.size() << " dofs generated  "<< std::endl;

  // Set up solution vectors...
  using V_R = Dune::PDELab::Backend::Vector<P1_dirichlet_GFS,DF>;
  V_R x_r(p1_dirichlet_gfs_);
  x_r = 0.0;
  auto lambda_0000 = [&](const auto& x){ return (double)x[1] * x[1] + x[0] * x[0]; };
  auto func_0000 = Dune::PDELab::makeGridFunctionFromCallable(gv, lambda_0000);
  Dune::PDELab::interpolate(func_0000, p1_dirichlet_gfs_, x_r);
  auto lambda_0001 = [&](const auto& x){ return 0.0; };
  auto func_0001 = Dune::PDELab::makeGridFunctionFromCallable(gv, lambda_0001);

  // Set up (non)linear solvers...
  using LinearSolver = Dune::PDELab::ISTLBackend_SEQ_SuperLU;
  using SLP = Dune::PDELab::StationaryLinearProblemSolver<GO_r, LinearSolver, V_R>;
  LinearSolver ls(false);
  double reduction = initree.get<double>("reduction", 1e-12);
  SLP slp(go_r, ls, x_r, reduction);
  slp.apply();

  // Do visualization...
  using VTKWriter = Dune::SubsamplingVTKWriter<GV>;
  Dune::RefinementIntervals subint(initree.get<int>("vtk.subsamplinglevel", 1));
  VTKWriter vtkwriter(gv, subint);
  std::string vtkfile = initree.get<std::string>("wrapper.vtkcompare.name", "output");
  CuttingPredicate predicate;
  Dune::PDELab::addSolutionToVTKWriter(vtkwriter, p1_dirichlet_gfs_, x_r, Dune::PDELab::vtk::defaultNameScheme(), predicate);
  vtkwriter.write(vtkfile, Dune::VTK::ascii);


  //===============================================================//
  //    ___      _ _       _       _     _____ _          __  __   //
  //   / _ \    | (_)     (_)     | |   /  ___| |        / _|/ _|  //
  //  / /_\ \ __| |_  ___  _ _ __ | |_  \ `--.| |_ _   _| |_| |_   //
  //  |  _  |/ _` | |/ _ \| | '_ \| __|  `--. \ __| | | |  _|  _|  //
  //  | | | | (_| | | (_) | | | | | |_  /\__/ / |_| |_| | | | |    //
  //  \_| |_/\__,_| |\___/|_|_| |_|\__| \____/ \__|\__,_|_| |_|    //
  //             _/ |                                              //
  //            |__/                                               //
  //===============================================================//

  std::cout << std::endl << "Adjoint Stuff" << std::endl << std::endl;

  //=========//
  // Adjoint //
  //=========//

  // The adjoint needs the solution of the forward problem
  auto p_x_gfs = std::make_shared<P1_dirichlet_GFS> (p1_dirichlet_gfs_);
  auto p_x_r = std::make_shared<V_R> (x_r);

  // Local operator for adjoint problem
  using LOP_Adjoint = RAdjointOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, P1_dirichlet_GFS>;
  LOP_Adjoint lop_adjoint(p1_dirichlet_gfs_, p1_dirichlet_gfs_, initree);
  lop_adjoint.setCoefficient1(p_x_gfs, p_x_r);

  // Grid operator for adjoint problem
  using GO_Adjoint = Dune::PDELab::GridOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, LOP_Adjoint, MatrixBackend, DF, RangeType, RangeType, P1_dirichlet_GFS_CC, P1_dirichlet_GFS_CC>;
  GO_Adjoint go_adjoint(p1_dirichlet_gfs_, p1_dirichlet_gfs__cc, p1_dirichlet_gfs_, p1_dirichlet_gfs__cc, lop_adjoint, mb);

  // Boundary condition
  using V_Adjoint = GO_Adjoint::Traits::Domain;
  V_Adjoint x_adjoint(p1_dirichlet_gfs_);
  x_adjoint = 0.0;

  // Solve problem
  using SLP_Adjoint = Dune::PDELab::StationaryLinearProblemSolver<GO_Adjoint, LinearSolver, V_Adjoint>;
  SLP_Adjoint slp_adjoint(go_adjoint, ls, x_adjoint, reduction);
  slp_adjoint.apply();

  // print_l2_norm(p1_dirichlet_gfs_, x_adjoint, gv);
  using Dune::PDELab::Backend::native;
  std::cout << "Norm of adjoint vector: " << native(x_adjoint).two_norm() << std::endl;

  //=========//
  // Control //
  //=========//

  // The control problem needs the solution of the adjoint problem
  auto p_adjoint_gfs = std::make_shared<P1_dirichlet_GFS> (p1_dirichlet_gfs_);
  auto p_adjoint_x = std::make_shared<V_Adjoint> (x_adjoint);

  // Derivative of objective function w.r.t. the control
  using DJDM = std::vector<RangeType>;
  DJDM dJdm(7,0.0);

  // Local operator for control problem
  using LOP_Control = RControlOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, P1_dirichlet_GFS, DJDM>;
  LOP_Control lop_control(p1_dirichlet_gfs_, p1_dirichlet_gfs_, initree, dJdm);
  lop_control.setCoefficient1(p_adjoint_gfs, p_adjoint_x);

  // Grid operator for control problem
  //
  // Note: Create without contstraints container. We don't want to
  // apply any Dirichlet constraints here (this would mean setting the
  // corresponding values of the residual vector to zero).
  //
  // Note: Having a GFS that was constructed with dirichlet
  // constraints and then creating a GO without constraints works.
  using GO_Control = Dune::PDELab::GridOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, LOP_Control, MatrixBackend, DF, RangeType, RangeType>;
  GO_Control go_control(p1_dirichlet_gfs_, p1_dirichlet_gfs_, lop_control, mb);

  // Calculate dJdm
  using V_Control = GO_Control::Traits::Domain;
  V_Control r_control(p1_dirichlet_gfs_);
  r_control = 0.0;
  go_control.residual(x_r, r_control);

  //========================================//
  // Print derivative of objective function //
  //========================================//

  std::cout << std::endl;
  std::cout << "Derivatives of objective function: " << std::setprecision(20)
            << dJdm[0] << "  "
            << dJdm[1] << "  "
            << dJdm[2] << "  "
            << dJdm[3] << "  "
            << dJdm[4] << "  "
            << dJdm[5] << "  "
            << dJdm[6] << "  "
            << std::endl;
  std::cout << std::endl;

  //==================================================================================//
  //   _____          _    ___      _ _       _       _     _____ _          __  __   //
  //  |  ___|        | |  / _ \    | (_)     (_)     | |   /  ___| |        / _|/ _|  //
  //  | |__ _ __   __| | / /_\ \ __| |_  ___  _ _ __ | |_  \ `--.| |_ _   _| |_| |_   //
  //  |  __| '_ \ / _` | |  _  |/ _` | |/ _ \| | '_ \| __|  `--. \ __| | | |  _|  _|  //
  //  | |__| | | | (_| | | | | | (_| | | (_) | | | | | |_  /\__/ / |_| |_| | | | |    //
  //  \____/_| |_|\__,_| \_| |_/\__,_| |\___/|_|_| |_|\__| \____/ \__|\__,_|_| |_|    //
  //                                _/ |                                              //
  //                               |__/                                               //
  //==================================================================================//

  // Compare with results from doflin-adjoint:
  using std::abs;
  bool fail = false;
  if (abs(dJdm[0]- 0.02895684)>1e-3)
    fail = true;
  if (abs(dJdm[1]- 0.00173435)>1e-3)
    fail = true;
  if (abs(dJdm[2]- 0.00173435)>1e-3)
    fail = true;
  if (abs(dJdm[3]- 0.03019001)>1e-3)
    fail = true;
  if (abs(dJdm[4]- 0.05060596)>1e-3)
    fail = true;
  if (abs(dJdm[5]- -0.03072505)>1e-3)
    fail = true;
  if (abs(dJdm[6]- 0.0236605)>1e-3)
    fail = true;

  return fail;

}


#endif //GENERATED_POISSON_MC_DRIVER_HH
