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

#include "blockstructured_preconditioner_linear_elasticity_nn_rOperator_file.hh"
#include "blockstructured_preconditioner_linear_elasticity_nn_rCoarseOperator_file.hh"
#include "blockstructured_preconditioner_linear_elasticity_nn_interpolation_operator_file.hh"
#include "blockstructured_preconditioner_linear_elasticity_nn_restriction_operator_file.hh"
#include "blockstructured_preconditioner_linear_elasticity_nn_local_decomposition_operator_file.hh"


constexpr int NBLOCKS = 8;


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
  using FEM = Dune::PDELab::BlockstructuredQkLocalFiniteElementMap<GV, DF, RangeType, NBLOCKS>;
  FEM fem(gv);

  // Set up grid function spaces...
  using VB = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::none>;
  using DirichletConstraintsAssember = Dune::PDELab::ConformingDirichletConstraints;
  using GFS_Q1 = Dune::PDELab::GridFunctionSpace<GV, FEM, DirichletConstraintsAssember, VB>;
  GFS_Q1 gfs_q1(gv, fem);
  gfs_q1.name("gfs_q1");

  using GFS =Dune::PDELab::PowerGridFunctionSpace<GFS_Q1, 2, VB>;
  GFS gfs(gfs_q1);

  // Set up constraints container...
  using CC = GFS::ConstraintsContainer<RangeType>::Type;
  CC cc;
  cc.clear();
  auto bctype_leaf = Dune::PDELab::makeBoundaryConditionFromCallable(gv, [&](const auto& x){  return (std::abs(x[0]) < 1e-10 ? 1 : 0.0); });
  Dune::PDELab::CompositeConstraintsParameters bctype(bctype_leaf, bctype_leaf);
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
  using C_GFS_Q1 = Dune::PDELab::GridFunctionSpace<GV, C_FEM, DirichletConstraintsAssember>;
  C_GFS_Q1 c_gfs_q1(gv, c_fem);
  c_gfs_q1.name("c_gfs");

  using C_GFS =Dune::PDELab::PowerGridFunctionSpace<C_GFS_Q1, 2, VB>;
  C_GFS c_gfs(c_gfs_q1);

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
  X x_r(gfs);
  x_r = 0.0;

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

  SchurOperatorMatrixFree<GOP_SCHUR_APPLY, GOP_SCHUR_RHS, GOP_SCHUR_BACK_TRAFO, Decomposition, X>
    schurOperatorMatrixFree(gop_schur_apply, gop_schur_rhs, gop_schur_back_trafo, decomp);
  NeumannNeumann<GOP_NN, Decomposition, X> pre_nn(gop_nn, decomp);
  using CGC = CoarseGridCorrection<I, R, X>;
  PreconditionerWrapper<Decomposition, CGC> pre_coarse(decomp, interpolation, restriction, c_gfs, c_cc, c_lop);
  AdditiveTwoLevel pre_twoLevel(pre_nn, pre_coarse);
  SchurComplement schurComplement(schurOperatorMatrixFree, pre_twoLevel, false);

  X r(gfs, 0.0);
  gop.residual(x_r, r);
  // solve the jacobian system
  X z(gfs, 0.0);
  schurComplement.apply(z, r);
  x_r -= z;

  // Do visualization...
  using VTKWriter = Dune::SubsamplingVTKWriter<GV>;
  Dune::RefinementIntervals subint(initree.get<int>("vtk.subsamplinglevel", 8));
  VTKWriter vtkwriter(gv, subint);
  std::string vtkfile = initree.get<std::string>("wrapper.vtkcompare.name", "output");
  CuttingPredicate predicate;
  Dune::PDELab::addSolutionToVTKWriter(vtkwriter, gfs, x_r, Dune::PDELab::vtk::defaultNameScheme(), predicate);
  vtkwriter.write(vtkfile, Dune::VTK::ascii);

  return 0;
}
