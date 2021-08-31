#include"config.h"

#include "dune/common/parametertreeparser.hh"
#include "dune/pdelab/gridfunctionspace/gridfunctionadapter.hh"
#include "dune/pdelab/constraints/conforming.hh"
#include "dune/pdelab/backend/istl.hh"
#include "dune/pdelab/gridfunctionspace/vtk.hh"
#include "dune/common/parametertree.hh"
#include "dune/testtools/gridconstruction.hh"
#include "dune/pdelab/finiteelementmap/pkfem.hh"
#include <random>
#include "dune/pdelab/function/callableadapter.hh"
#include "dune/codegen/vtkpredicate.hh"
#include <string>
#include "dune/alugrid/grid.hh"
#include "dune/pdelab/common/functionutilities.hh"
#include "dune/pdelab/gridoperator/gridoperator.hh"
#include "dune/pdelab/stationary/linearproblem.hh"
#include "dune/grid/io/file/vtk/subsamplingvtkwriter.hh"
#include "dune/pdelab/function/discretegridviewfunction.hh"

#if OPERATOR == 1
#include "poisson_grad_localoperator.hh"
#endif

#if OPERATOR == 0
#include "poisson_nongrad_localoperator.hh"
#endif

int main(int argc, char** argv)
{
  // MPI helper stuff
  Dune::MPIHelper& helper = Dune::MPIHelper::instance(argc, argv);

  // Parse the ini file
  Dune::ParameterTree initree;
  Dune::ParameterTreeParser::readINITree(argv[1], initree);

  // Build a grid
  using Grid = Dune::ALUGrid<2, 2, Dune::simplex, Dune::conforming>;
  using GV = Grid::LeafGridView;
  IniGridFactory<Grid> factory(initree);
  std::shared_ptr<Grid> grid = factory.getGrid();
  GV gv = grid->leafGridView();

  // General types and stuff
  using DF = Grid::ctype;
  using RangeType = double;

  // Finite Element Maps
  using P1_FEM = Dune::PDELab::PkLocalFiniteElementMap<GV, DF, RangeType, 1>;
  using P2_FEM = Dune::PDELab::PkLocalFiniteElementMap<GV, DF, RangeType, 2>;
  P1_FEM p1_fem(gv);
  P2_FEM p2_fem(gv);

  // Grid Function Spaces
  using VectorBackend = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::none>;
  using DirichletConstraintsAssember = Dune::PDELab::ConformingDirichletConstraints;
  using P1_dirichlet_GFS = Dune::PDELab::GridFunctionSpace<GV, P1_FEM, DirichletConstraintsAssember, VectorBackend>;
  P1_dirichlet_GFS p1_dirichlet_gfs_(gv, p1_fem);
  p1_dirichlet_gfs_.name("p1_dirichlet_gfs_");
  p1_dirichlet_gfs_.update();
  std::cout << "gfs with " << p1_dirichlet_gfs_.size() << " dofs generated  "<< std::endl;

  // Solution vectors / Grid Functions
  using V_R = Dune::PDELab::Backend::Vector<P1_dirichlet_GFS,DF>;
  V_R x_r(p1_dirichlet_gfs_);

  // GFS and coefficient vector of FE-fct that will be passed to lop
  using P2_GFS = Dune::PDELab::GridFunctionSpace<GV, P2_FEM, DirichletConstraintsAssember, VectorBackend>;
  using V2 = Dune::PDELab::Backend::Vector<P2_GFS,DF>;
  auto p_coeff_gfs = std::make_shared<P2_GFS> (gv, p2_fem);
  auto p_coeff_vec = std::make_shared<V2> (*p_coeff_gfs);

  // Local Operator
  using LOP_R = PoissonLocalOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, P2_GFS>;
  LOP_R lop_r(p1_dirichlet_gfs_, p1_dirichlet_gfs_, initree);
  lop_r.setCoefficient1(p_coeff_gfs, p_coeff_vec);

  // Constraints stuff
  using P1_dirichlet_GFS_CC = P1_dirichlet_GFS::ConstraintsContainer<RangeType>::Type;
  P1_dirichlet_GFS_CC p1_dirichlet_gfs__cc;
  p1_dirichlet_gfs__cc.clear();
  auto p1_bctype_lambda = [&](const auto& x){ return 1.0; };
  auto p1_bctype = Dune::PDELab::makeBoundaryConditionFromCallable(gv, p1_bctype_lambda);
  Dune::PDELab::constraints(p1_bctype, p1_dirichlet_gfs_, p1_dirichlet_gfs__cc);
  std::cout << "cc with " << p1_dirichlet_gfs__cc.size() << " dofs generated  "<< std::endl;

  // Matrix Backend
  using MatrixBackend = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
  int generic_dof_estimate =  6 * p1_dirichlet_gfs_.maxLocalSize();
  int dofestimate = initree.get<int>("istl.number_of_nnz", generic_dof_estimate);
  MatrixBackend mb(dofestimate);

  // Grid Operator
  using GO_r = Dune::PDELab::GridOperator<P1_dirichlet_GFS, P1_dirichlet_GFS, LOP_R, MatrixBackend, DF, RangeType, RangeType, P1_dirichlet_GFS_CC, P1_dirichlet_GFS_CC>;
  GO_r go_r(p1_dirichlet_gfs_, p1_dirichlet_gfs__cc, p1_dirichlet_gfs_, p1_dirichlet_gfs__cc, lop_r, mb);

  // Solver
  using LinearSolver = Dune::PDELab::ISTLBackend_SEQ_SuperLU;
  LinearSolver ls(false);
  using SLP = Dune::PDELab::StationaryLinearProblemSolver<GO_r, LinearSolver, V_R>;

  // Interpolation
  auto lambda_0000 = [&](const auto& x){ return (double)exp((-1.0) * ((0.5 - x[1]) * (0.5 - x[1]) + (0.5 - x[0]) * (0.5 - x[0]))); };
  auto func_0000 = Dune::PDELab::makeGridFunctionFromCallable(gv, lambda_0000);
  Dune::PDELab::interpolate(func_0000, p1_dirichlet_gfs_, x_r);

  auto lambda_0001 = [&](const auto& x){ return (0.5-x[0])*(0.5-x[0]) + (0.5-x[1])*(0.5-x[1]); };
  auto func_0001 = Dune::PDELab::makeGridFunctionFromCallable(gv, lambda_0001);
  Dune::PDELab::interpolate(func_0001, *p_coeff_gfs, *p_coeff_vec);

  // Solving
  double reduction = initree.get<double>("reduction", 1e-12);
  SLP slp(go_r, ls, x_r, reduction);
  slp.apply();

  // VTK visualization
  using VTKWriter = Dune::SubsamplingVTKWriter<GV>;
  Dune::RefinementIntervals subint(initree.get<int>("vtk.subsamplinglevel", 1));
  VTKWriter vtkwriter(gv, subint);
  std::string vtkfile = initree.get<std::string>("wrapper.vtkcompare.name", "output");
  CuttingPredicate predicate;
  Dune::PDELab::addSolutionToVTKWriter(vtkwriter, p1_dirichlet_gfs_, x_r, Dune::PDELab::vtk::defaultNameScheme(), predicate);
  vtkwriter.write(vtkfile, Dune::VTK::ascii);

  // Error calculation
  using P1_DIRICHLET_GFS__DGF = Dune::PDELab::DiscreteGridFunction<decltype(p1_dirichlet_gfs_),decltype(x_r)>;
  P1_DIRICHLET_GFS__DGF p1_dirichlet_gfs__dgf(p1_dirichlet_gfs_,x_r);
  using DifferenceSquaredAdapter_ = Dune::PDELab::DifferenceSquaredAdapter<decltype(func_0000), decltype(p1_dirichlet_gfs__dgf)>;
  DifferenceSquaredAdapter_ dsa_(func_0000, p1_dirichlet_gfs__dgf);
  RangeType l2error(0.0);
  {
    // L2 error squared of difference between numerical
    // solution and the interpolation of exact solution
    // for treepath ()
    typename P1_DIRICHLET_GFS__DGF::Traits::RangeType err(0.0);
    Dune::PDELab::integrateGridFunction(dsa_, err, 10);

    l2error += err;
    if (gv.comm().rank() == 0){
      std::cout << "L2 Error for treepath : " << err << std::endl;
    }}
  bool testfail(false);
  using std::abs;
  using std::isnan;
  if (gv.comm().rank() == 0){
    std::cout << "\nl2errorsquared: " << l2error << std::endl << std::endl;
  }
  if (isnan(l2error) or abs(l2error)>1e-7)
    testfail = true;
  return testfail;
}
