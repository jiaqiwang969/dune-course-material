#include "config.h"
#include "dune/common/parallel/mpihelper.hh"
#include "dune/pdelab/stationary/linearproblem.hh"
#include "dune/pdelab/backend/istl.hh"
#include "dune/grid/uggrid.hh"
#include "dune/grid/yaspgrid.hh"
#include "dune/pdelab/finiteelementmap/qkdg.hh"
#include "poisson_dg_3d_facedir_facemod_variation_deg1_symdiff_nonquadvec_nongradvec_rOperator_file.hh"
#include "dune/pdelab/gridoperator/gridoperator.hh"
#include "dune/testtools/gridconstruction.hh"
#include "dune/common/parametertree.hh"
#include "dune/common/parametertreeparser.hh"
#include "dune/consistent-edge-orientation/createconsistentgrid.hh"
#include <random>
#include "dune/pdelab/gridfunctionspace/vtk.hh"
#include "dune/grid/io/file/vtk/subsamplingvtkwriter.hh"
#include "string"
#include "dune/codegen/vtkpredicate.hh"
#include "dune/pdelab/function/callableadapter.hh"
#include "dune/pdelab/gridfunctionspace/gridfunctionadapter.hh"
#include "dune/pdelab/common/functionutilities.hh"

template <typename T>
bool isclose(T a, T b, double rel_tol=1e-9, double abs_tol=0.0){
  // Basically a python isclose (PEP 485) without error checking...
  return std::abs(a-b) <= std::max(rel_tol*std::max(std::abs(a), std::abs(b)), abs_tol);
}

template<typename T>
bool fuzzy_is_permutation(T a, T b, double rel_tol=1e-9, double abs_tol=1e-14){
  assert (a.size()==b.size());
  std::sort(a.begin(), a.end());
  std::sort(b.begin(), b.end());

  for (std::size_t i=0; i<a.size(); ++i){
    if (!isclose(a[i], b[i], rel_tol, abs_tol))
      return false;
  }
  return true;
}



template<typename GV>
void test_grid(GV gv){
  // iterate over all entities of the grid
  for (const auto& e : elements(gv))
  {
    std::cout << "## New Element!" << std::endl;
    auto geo = e.geometry();
    for (int i=0; i<geo.corners(); i++){
      auto global_corner = geo.corner(i);
      auto local_corner = geo.local(global_corner);
      std::cout << "global_corner: ";
      for (int i=0; i<3; ++i)
        std::cout << global_corner[i] << " ";
      std::cout << std::endl;
    }
    for (int i=0; i<geo.corners(); i++){
      auto global_corner = geo.corner(i);
      auto local_corner = geo.local(global_corner);
      std::cout << "local_corner: ";
      for (int i=0; i<3; ++i)
        std::cout << local_corner[i] << " ";
      std::cout << std::endl;
    }
  }
}

int main(int argc, char** argv){
  try
  {
    // Initialize basic stuff...
    Dune::MPIHelper& mpihelper = Dune::MPIHelper::instance(argc, argv);
    using RangeType = double;
    Dune::ParameterTree initree;
    Dune::ParameterTreeParser::readINITree(argv[1], initree);

    // Setup grid (view)...
    using Grid = Dune::UGGrid<3>;
    // using Grid = Dune::ALUGrid<3,3,Dune::cube,Dune::nonconforming>;

    using GV = Grid::LeafGridView;
    using DF = Grid::ctype;

    // Gmsh
    IniGridFactory<Grid> factory(initree);
    std::shared_ptr<Grid> grid_nonconsistent = factory.getGrid();
    std::shared_ptr<Grid> grid = createConsistentGrid(grid_nonconsistent);
    GV gv = grid->leafGridView();

    test_grid(gv);

    // Set up finite element maps...
    using DG1_FEM = Dune::PDELab::QkDGLocalFiniteElementMap<DF, RangeType, 1, 3>;
    DG1_FEM dg1_fem;

    // Set up grid function spaces...
    using VectorBackendDG1 = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::none>;
    using NoConstraintsAssembler = Dune::PDELab::NoConstraints;
    using DG1_GFS = Dune::PDELab::GridFunctionSpace<GV, DG1_FEM, NoConstraintsAssembler, VectorBackendDG1>;
    DG1_GFS dg1_gfs_(gv, dg1_fem);
    dg1_gfs_.name("dg1_gfs_");

    // Set up constraints container...
    using DG1_GFS_CC = DG1_GFS::ConstraintsContainer<RangeType>::Type;
    DG1_GFS_CC dg1_gfs__cc;
    dg1_gfs__cc.clear();
    Dune::PDELab::constraints(dg1_gfs_, dg1_gfs__cc);

    // Set up grid grid operators...
    using LOP_R = rOperator<DG1_GFS, DG1_GFS>;
    using MatrixBackend = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
    using GO_r = Dune::PDELab::GridOperator<DG1_GFS, DG1_GFS, LOP_R, MatrixBackend, DF, RangeType, RangeType, DG1_GFS_CC, DG1_GFS_CC>;
    LOP_R lop_r(dg1_gfs_, dg1_gfs_, initree);
    dg1_gfs_.update();
    int generic_dof_estimate =  8 * dg1_gfs_.maxLocalSize();
    int dofestimate = initree.get<int>("istl.number_of_nnz", generic_dof_estimate);
    MatrixBackend mb(dofestimate);
    GO_r go_r(dg1_gfs_, dg1_gfs__cc, dg1_gfs_, dg1_gfs__cc, lop_r, mb);
    std::cout << "gfs with " << dg1_gfs_.size() << " dofs generated  "<< std::endl;
    std::cout << "cc with " << dg1_gfs__cc.size() << " dofs generated  "<< std::endl;

    // Set up solution vectors...
    using V_R = Dune::PDELab::Backend::Vector<DG1_GFS,DF>;
    V_R x_r(dg1_gfs_);
    x_r = 0.0;
    auto lambda_0000 = [&](const auto& is, const auto& xl){ auto x=is.geometry().global(xl); return exp((-1.0) * ((0.5 - x[2]) * (0.5 - x[2]) + (0.5 - x[1]) * (0.5 - x[1]) + (0.5 - x[0]) * (0.5 - x[0])));; };
    auto func_0000 = Dune::PDELab::makeGridFunctionFromCallable(gv, lambda_0000);

    // Set up (non)linear solvers...
    using LinearSolver = Dune::PDELab::ISTLBackend_SEQ_SuperLU;
    using SLP = Dune::PDELab::StationaryLinearProblemSolver<GO_r, LinearSolver, V_R>;
    LinearSolver ls(false);
    double reduction = initree.get<double>("reduction", 1e-12);
    SLP slp(go_r, ls, x_r, reduction);
    //  slp.apply();

    // Do visualization...
    using VTKWriter = Dune::SubsamplingVTKWriter<GV>;
    Dune::RefinementIntervals subint(initree.get<int>("vtk.subsamplinglevel", 1));
    VTKWriter vtkwriter(gv, subint);
    std::string vtkfile = initree.get<std::string>("wrapper.vtkcompare.name", "output");
    CuttingPredicate predicate;
    Dune::PDELab::addSolutionToVTKWriter(vtkwriter, dg1_gfs_, x_r, Dune::PDELab::vtk::defaultNameScheme(), predicate);
    vtkwriter.write(vtkfile, Dune::VTK::ascii);

    // Maybe print residuals and matrices to stdout...
    if (initree.get<bool>("printresidual", false)) {
      using Dune::PDELab::Backend::native;
      V_R x_s(x_r);
      // Interpolate input
      auto interpolate_lambda =
        [] (const auto& e, const auto& xl){
          auto xg = e.geometry().global(xl);
          auto center = e.geometry().center();
          if (center.two_norm() < 2){
            return std::sin((xg.two_norm2()+xg[0]/3)/10);
          }
          else{
            return std::sin((xg.two_norm2())/10);
          }
        };
      auto interpolate = Dune::PDELab::makeGridFunctionFromCallable(gv, interpolate_lambda);
      Dune::PDELab::interpolate(interpolate,dg1_gfs_,x_s);
      Dune::printvector(std::cout, native(x_s), "x_s", "row");

      V_R r(x_r);
      r=0.0;
      go_r.residual(x_s, r);
      Dune::printvector(std::cout, native(r), "residual vector", "row");

      // std::cout.precision(17);
      std::vector<RangeType> residual(16);
      for (std::size_t i=0; i<16; ++i){
        residual[i] = native(r)[i];
      }
      std::cout << "Residual:" << std::endl;
      std::cout.precision(17);
      for (std::size_t i=0; i<16; ++i){
        std::cout << residual[i] << ", ";
      }
      std::cout << std::endl;
    }
    if (initree.get<bool>("printmatrix", false)) {
      using Dune::PDELab::Backend::native;
      V_R r(x_r);
      // Interpolate input
      auto interpolate_lambda = [] (const auto& x){
        return std::exp(x[0]*x[0]+x[1]*x[1]+x[2]*x[2]);
      };
      auto interpolate = Dune::PDELab::makeGridFunctionFromCallable(gv, interpolate_lambda);
      Dune::PDELab::interpolate(interpolate,dg1_gfs_,x_r);
      using M = typename GO_r::Traits::Jacobian;
      M m(go_r);
      go_r.jacobian(x_r,m);
      using Dune::PDELab::Backend::native;
      Dune::printmatrix(std::cout, native(m),"global stiffness matrix","row",9,1);
    }

    // // Maybe calculate errors for test results...
    // using DG1_GFS__DGF = Dune::PDELab::DiscreteGridFunction<decltype(dg1_gfs_),decltype(x_r)>;
    // DG1_GFS__DGF dg1_gfs__dgf(dg1_gfs_,x_r);
    // using DifferenceSquaredAdapter_ = Dune::PDELab::DifferenceSquaredAdapter<decltype(func_0000), decltype(dg1_gfs__dgf)>;
    // DifferenceSquaredAdapter_ dsa_(func_0000, dg1_gfs__dgf);
    // Dune::FieldVector<RangeType, 1> l2error(0.0);
    // {
    //   // L2 error squared of difference between numerical
    //   // solution and the interpolation of exact solution
    //   // for treepath ()
    //   typename decltype(dsa_)::Traits::RangeType err(0.0);
    //   Dune::PDELab::integrateGridFunction(dsa_, err, 10);

    //   l2error += err;
    //   if (gv.comm().rank() == 0){
    //     std::cout << "L2 Error for treepath : " << err << std::endl;
    //   }}
    // bool testfail(false);
    // using std::abs;
    // using std::isnan;
    // if (gv.comm().rank() == 0){
    //   std::cout << "\nl2errorsquared: " << l2error << std::endl << std::endl;
    // }
    // if (isnan(l2error[0]) or abs(l2error[0])>1e-4)
    //   testfail = true;
    // return testfail;
    return 0;

  }
  catch (Dune::Exception& e)
  {    std::cerr << "Dune reported error: " << e << std::endl;
    return 1;
  }
  catch (std::exception& e)
  {    std::cerr << "Unknown exception thrown!" << std::endl;
    return 1;
  }
}
