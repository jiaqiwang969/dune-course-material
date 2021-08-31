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

#include "blockstructured_preconditioner_poisson_nn_rOperator_file.hh"
#include "blockstructured_preconditioner_poisson_nn_rCoarseOperator_file.hh"
#include "blockstructured_preconditioner_poisson_nn_interpolation_operator_file.hh"
#include "blockstructured_preconditioner_poisson_nn_restriction_operator_file.hh"
#include "blockstructured_preconditioner_poisson_nn_local_decomposition_operator_file.hh"


constexpr int NBLOCKS = 8;
constexpr int DEGREE = 1;


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

  using LS = IterativeMatrixFreeLocalSolver<GV, LOP, RangeType, LocalDecompositionOperator<GFS, GFS>, NBLOCKS>;
  LS ls(gv, gfs, lop);

  using LOP_NN = NeumannNeumannOperator<GV, LS, RangeType, NBLOCKS>;
  using GOP_NN = Dune::PDELab::GridOperator<GFS, GFS, LOP_NN, MB, DF, RangeType, RangeType, CC, CC>;
  LOP_NN lop_nn(gv, ls);
  GOP_NN gop_nn(gfs, cc, gfs, cc, lop_nn, mb);

  using LOP_SCHUR_APPLY = SchurApplyOperator<GV, LS, RangeType, NBLOCKS>;
  using GOP_SCHUR_APPLY = Dune::PDELab::GridOperator<GFS, GFS, LOP_SCHUR_APPLY, MB, DF, RangeType, RangeType, CC, CC>;
  LOP_SCHUR_APPLY lop_schur_apply(gv, ls);
  GOP_SCHUR_APPLY gop_schur_apply(gfs, cc, gfs, cc, lop_schur_apply, mb);

  using LOP_SCHUR_RHS = SchurRHSOperator<GV, LS, RangeType, NBLOCKS>;
  using GOP_SCHUR_RHS = Dune::PDELab::GridOperator<GFS, GFS, LOP_SCHUR_RHS, MB, DF, RangeType, RangeType, CC, CC>;
  LOP_SCHUR_RHS lop_schur_rhs(gv, ls);
  GOP_SCHUR_RHS gop_schur_rhs(gfs, cc, gfs, cc, lop_schur_rhs, mb);

  using LOP_SCHUR_BACK_TRAFO = SchurBackTrafoOperator<GV, LS, RangeType, NBLOCKS>;
  using GOP_SCHUR_BACK_TRAFO = Dune::PDELab::GridOperator<GFS, GFS, LOP_SCHUR_BACK_TRAFO, MB, DF, RangeType, RangeType, CC, CC>;
  LOP_SCHUR_BACK_TRAFO lop_schur_back_trafo(gv, ls);
  GOP_SCHUR_BACK_TRAFO gop_schur_back_trafo(gfs, cc, gfs, cc, lop_schur_back_trafo, mb);

  const bool only_preconditioning = initree.get<bool>("only_preconditioning", false);

  SchurOperatorMatrixFree<GOP_SCHUR_APPLY, GOP_SCHUR_RHS, GOP_SCHUR_BACK_TRAFO, Decomposition, X>
    schurOperatorMatrixFree(gop_schur_apply, gop_schur_rhs, gop_schur_back_trafo, decomp);
  NeumannNeumann<GOP_NN, Decomposition, X> pre_nn(gop_nn, decomp);

  using CGC = CoarseGridCorrection<I, R, X>;
  std::unique_ptr<Dune::Preconditioner<X, X>> pre_coarse_ptr{};
  if(only_preconditioning)
    pre_coarse_ptr = std::make_unique<CGC>(interpolation, restriction, c_gfs, c_cc, c_lop);
  else
    pre_coarse_ptr = std::make_unique<PreconditionerWrapper<Decomposition, CGC>>(
        decomp, interpolation, restriction, c_gfs, c_cc, c_lop
    );

  AdditiveTwoLevel pre_twoLevel(pre_nn, *pre_coarse_ptr);
  SchurComplement schurComplement(schurOperatorMatrixFree, pre_twoLevel, only_preconditioning);

  if(only_preconditioning){
    Dune::PDELab::solveMatrixFree(gop, x_r, schurComplement);
  } else {
    X r(gfs, 0.0);
    gop.residual(x_r, r);
    // solve the jacobian system
    X z(gfs, 0.0);
    schurComplement.apply(z, r);
    x_r -= z;
  }

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
