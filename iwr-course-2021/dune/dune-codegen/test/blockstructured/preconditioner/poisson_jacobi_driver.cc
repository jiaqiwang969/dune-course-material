#include "config.h"

#include <string>
#include "dune/common/parallel/mpihelper.hh"
#include "dune/common/parametertree.hh"
#include "dune/common/parametertreeparser.hh"
#include "dune/grid/yaspgrid.hh"
#include "dune/grid/io/file/vtk/subsamplingvtkwriter.hh"
#include "dune/pdelab/constraints/conforming.hh"
#include "dune/pdelab/gridoperator/gridoperator.hh"
#include "dune/pdelab/function/callableadapter.hh"
#include "dune/pdelab/common/functionutilities.hh"
#include "dune/pdelab/stationary/linearproblem.hh"
#include "dune/pdelab/gridfunctionspace/vtk.hh"
#include "dune/pdelab/gridfunctionspace/gridfunctionadapter.hh"
#include "dune/testtools/gridconstruction.hh"
#include "dune/codegen/matrixfree.hh"
#include "dune/codegen/blockstructured/blockstructuredqkfem.hh"
#include "dune/codegen/blockstructured/preconditioner/preconditioner.hh"
#include "dune/codegen/vtkpredicate.hh"

#include "blockstructured_preconditioner_poisson_jacobi_rOperator_file.hh"
#include "blockstructured_preconditioner_poisson_jacobi_rCoarseOperator_file.hh"
#include "blockstructured_preconditioner_poisson_jacobi_rPointDiagonal_file.hh"
#include "blockstructured_preconditioner_poisson_jacobi_interpolation_operator_file.hh"
#include "blockstructured_preconditioner_poisson_jacobi_restriction_operator_file.hh"


constexpr int NBLOCKS = 8;
constexpr int DEGREE = 2;

int main(int argc, char** argv){
  // Initialize basic stuff...
  Dune::MPIHelper::instance(argc, argv);
  using RangeType = double;
  Dune::ParameterTree initree;
  Dune::ParameterTreeParser::readINITree(argv[1], initree);

  // Setup grid (view)...
  using Grid = Dune::YaspGrid<2, Dune::EquidistantCoordinates<RangeType, 2>>;
  using GV = Grid::LeafGridView;
  using DF = Grid::ctype;
  IniGridFactory<Grid> factory(initree);
  std::shared_ptr<Grid> grid = factory.getGrid();
  GV gv = grid->leafGridView();

  // Set up finite element maps...
  using FEM = Dune::PDELab::BlockstructuredQkLocalFiniteElementMap<GV, DF, RangeType, NBLOCKS * DEGREE>;
  FEM fem(gv);

  // Set up grid function spaces...
  using VB = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::none>;
  using DirichletConstraintsAssember = Dune::PDELab::ConformingDirichletConstraints;
  using GFS = Dune::PDELab::GridFunctionSpace<GV, FEM, DirichletConstraintsAssember, VB>;
  GFS gfs(gv, fem);
  gfs.name("gfs");

  // Set up constraints container...
  using CC = GFS::ConstraintsContainer<RangeType>::Type;
  CC cc;
  cc.clear();
  auto bctype_lambda = [&](const auto& x){ return 1.0; };
  auto bctype = Dune::PDELab::makeBoundaryConditionFromCallable(gv, bctype_lambda);
  Dune::PDELab::constraints(bctype, gfs, cc);

  // Set up grid grid operators...
  using LOP = rOperator<GFS, GFS>;
  using MB = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
  using GOP = Dune::PDELab::GridOperator<GFS, GFS, LOP, MB, DF, RangeType, RangeType, CC, CC>;
  LOP lop(gfs, gfs, initree);
  gfs.update();
  MB mb(9);
  GOP gop(gfs, cc, gfs, cc, lop, mb);
  std::cout << "gfs with " << gfs.size() << " dofs generated  "<< std::endl;
  std::cout << "cc with " << cc.size() << " dofs generated  "<< std::endl;

  // Set up finite element maps...
  using C_FEM = Dune::PDELab::BlockstructuredQkLocalFiniteElementMap<GV, DF, RangeType, 1>;
  C_FEM c_fem(gv);

  // Set up grid function spaces...
  using C_GFS = Dune::PDELab::GridFunctionSpace<GV, C_FEM, DirichletConstraintsAssember>;
  C_GFS c_gfs(gv, c_fem);
  c_gfs.name("c_gfs");

  // Set up constraints container...
  using C_CC = C_GFS::ConstraintsContainer<RangeType>::Type;
  C_CC c_cc;
  c_cc.clear();
  Dune::PDELab::constraints(bctype, c_gfs, c_cc);
  std::cout << "c_gfs with " << c_gfs.size() << " dofs generated  "<< std::endl;
  std::cout << "c_cc with " << c_cc.size() << " dofs generated  "<< std::endl;

  // Set up grid grid operators...
  using C_LOP = rCoarseOperator<C_GFS, C_GFS>;
  C_LOP c_lop(c_gfs, c_gfs, initree);
  c_gfs.update();

  // Set up solution vectors...
  using X = Dune::PDELab::Backend::Vector<GFS,DF>;
  using J = Dune::PDELab::Backend::Matrix<MB,X,X,RangeType>;
  using M = Dune::PDELab::Backend::Native<J>;
  X x_r(gfs), z(gfs);
  x_r = 0.0;
  auto lambda_0000 = [&](const auto& x){ return (double)x[1] * x[1] + x[0] * x[0]; };
  auto func_0000 = Dune::PDELab::makeGridFunctionFromCallable(gv, lambda_0000);
  Dune::PDELab::interpolate(func_0000, gfs, x_r);

  SchurDecomposition<GFS, CC> decomp(gfs, cc);
  using Decomposition = decltype(decomp);

  RestrictionLocalOperator<GFS, GFS> r_lop(gfs, gfs, initree);
  RestrictionOperator restriction(r_lop, gfs, cc, c_gfs, c_cc, decomp);
  using R = decltype(restriction);

  InterpolationLocalOperator<GFS, GFS> i_lop(gfs, gfs, initree);
  InterpolationOperator interpolation(i_lop, gfs, cc, c_gfs, c_cc, decomp);
  using I = decltype(interpolation);

  rPointDiagonal<GFS, GFS> point_diagonal_lop(gfs, gfs, initree);
  using PointDiagonalGOP = Dune::PDELab::GridOperator<GFS, GFS, rPointDiagonal<GFS, GFS>, MB, DF, RangeType, RangeType>;
  PointDiagonalGOP point_diagonal_gop(gfs, gfs, point_diagonal_lop, mb);
  X point_diagonal(gfs, 0.), zero(gfs, 0.);
  point_diagonal_gop.residual(zero, point_diagonal);

  DiagonalMatrixInverse<X> inverse_diagonal(point_diagonal);
  Dune::PDELab::OnTheFlyOperator<X, X, GOP> op(gop);

  JacobiPreconditioner<X> pre_jacobi(op, inverse_diagonal);

  CoarseGridCorrection<I, R, X> pre_coarse(interpolation, restriction, c_gfs, c_cc, c_lop);

  AdditiveTwoLevel pre_twoLevel(pre_jacobi, pre_coarse);

  Dune::PDELab::solveMatrixFree(gop, x_r, pre_twoLevel);

  // Maybe calculate errors for test results...
  auto exact_solution = func_0000;
  using DiscreteGridFunction_ = Dune::PDELab::DiscreteGridFunction<GFS, X>;
  DiscreteGridFunction_ discreteGridFunction_(gfs, x_r);
  using DifferenceSquaredAdapter_ = Dune::PDELab::DifferenceSquaredAdapter<decltype(exact_solution), DiscreteGridFunction_>;
  DifferenceSquaredAdapter_ dsa_(exact_solution, discreteGridFunction_);
  Dune::FieldVector<RangeType, 1> l2error(0.0);
  {
    // L2 error squared of difference between numerical
    // solution and the interpolation of exact solution
    // for treepath ()
    typename decltype(dsa_)::Traits::RangeType err(0.0);
    Dune::PDELab::integrateGridFunction(dsa_, err, 10);

    l2error += err;
    if (gv.comm().rank() == 0){
      std::cout << "L2 Error for treepath : " << err << std::endl;
    }
  }
  if (isnan(l2error[0]) or abs(l2error[0])>1e-7)
    return 1;
  else
    return 0;
}
