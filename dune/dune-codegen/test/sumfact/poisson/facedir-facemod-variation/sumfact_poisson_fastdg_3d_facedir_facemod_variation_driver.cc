#include "config.h"
#include "dune/common/parallel/mpihelper.hh"
#include "dune/pdelab/stationary/linearproblem.hh"
#include "dune/pdelab/backend/istl.hh"
#include "dune/pdelab/finiteelement/qkdglagrange.hh"
#include "dune/grid/uggrid.hh"
#include "dune/grid/yaspgrid.hh"
#include "dune/pdelab/finiteelementmap/qkdg.hh"
#include "dune/pdelab/gridoperator/fastdg.hh"
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

#if MSH_VARIANT == 0 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh00_nongradvec.hh"
#elif MSH_VARIANT == 1 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh01_nongradvec.hh"
#elif MSH_VARIANT == 2 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh02_nongradvec.hh"
#elif MSH_VARIANT == 3 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh03_nongradvec.hh"
#elif MSH_VARIANT == 4 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh04_nongradvec.hh"
#elif MSH_VARIANT == 5 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh05_nongradvec.hh"
#elif MSH_VARIANT == 6 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh06_nongradvec.hh"
#elif MSH_VARIANT == 7 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh07_nongradvec.hh"
#elif MSH_VARIANT == 8 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh08_nongradvec.hh"
#elif MSH_VARIANT == 9 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh09_nongradvec.hh"
#elif MSH_VARIANT == 10 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh10_nongradvec.hh"
#elif MSH_VARIANT == 11 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh11_nongradvec.hh"
#elif MSH_VARIANT == 12 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh12_nongradvec.hh"
#elif MSH_VARIANT == 13 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh13_nongradvec.hh"
#elif MSH_VARIANT == 14 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh14_nongradvec.hh"
#elif MSH_VARIANT == 15 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh15_nongradvec.hh"
#elif MSH_VARIANT == 16 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh16_nongradvec.hh"
#elif MSH_VARIANT == 17 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh17_nongradvec.hh"
#elif MSH_VARIANT == 18 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh18_nongradvec.hh"
#elif MSH_VARIANT == 19 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh19_nongradvec.hh"
#elif MSH_VARIANT == 20 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh20_nongradvec.hh"
#elif MSH_VARIANT == 21 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh21_nongradvec.hh"
#elif MSH_VARIANT == 22 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh22_nongradvec.hh"
#elif MSH_VARIANT == 23 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh23_nongradvec.hh"
#elif MSH_VARIANT == 24 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh24_nongradvec.hh"
#elif MSH_VARIANT == 25 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh25_nongradvec.hh"
#elif MSH_VARIANT == 26 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh26_nongradvec.hh"
#elif MSH_VARIANT == 27 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh27_nongradvec.hh"
#elif MSH_VARIANT == 28 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh28_nongradvec.hh"
#elif MSH_VARIANT == 29 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh29_nongradvec.hh"
#elif MSH_VARIANT == 30 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh30_nongradvec.hh"
#elif MSH_VARIANT == 31 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh31_nongradvec.hh"
#elif MSH_VARIANT == 32 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh32_nongradvec.hh"
#elif MSH_VARIANT == 33 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh33_nongradvec.hh"
#elif MSH_VARIANT == 34 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh34_nongradvec.hh"
#elif MSH_VARIANT == 35 && GRADVEC == 0
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh35_nongradvec.hh"
#elif MSH_VARIANT == 0 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh00_gradvec.hh"
#elif MSH_VARIANT == 1 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh01_gradvec.hh"
#elif MSH_VARIANT == 2 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh02_gradvec.hh"
#elif MSH_VARIANT == 3 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh03_gradvec.hh"
#elif MSH_VARIANT == 4 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh04_gradvec.hh"
#elif MSH_VARIANT == 5 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh05_gradvec.hh"
#elif MSH_VARIANT == 6 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh06_gradvec.hh"
#elif MSH_VARIANT == 7 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh07_gradvec.hh"
#elif MSH_VARIANT == 8 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh08_gradvec.hh"
#elif MSH_VARIANT == 9 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh09_gradvec.hh"
#elif MSH_VARIANT == 10 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh10_gradvec.hh"
#elif MSH_VARIANT == 11 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh11_gradvec.hh"
#elif MSH_VARIANT == 12 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh12_gradvec.hh"
#elif MSH_VARIANT == 13 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh13_gradvec.hh"
#elif MSH_VARIANT == 14 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh14_gradvec.hh"
#elif MSH_VARIANT == 15 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh15_gradvec.hh"
#elif MSH_VARIANT == 16 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh16_gradvec.hh"
#elif MSH_VARIANT == 17 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh17_gradvec.hh"
#elif MSH_VARIANT == 18 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh18_gradvec.hh"
#elif MSH_VARIANT == 19 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh19_gradvec.hh"
#elif MSH_VARIANT == 20 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh20_gradvec.hh"
#elif MSH_VARIANT == 21 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh21_gradvec.hh"
#elif MSH_VARIANT == 22 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh22_gradvec.hh"
#elif MSH_VARIANT == 23 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh23_gradvec.hh"
#elif MSH_VARIANT == 24 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh24_gradvec.hh"
#elif MSH_VARIANT == 25 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh25_gradvec.hh"
#elif MSH_VARIANT == 26 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh26_gradvec.hh"
#elif MSH_VARIANT == 27 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh27_gradvec.hh"
#elif MSH_VARIANT == 28 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh28_gradvec.hh"
#elif MSH_VARIANT == 29 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh29_gradvec.hh"
#elif MSH_VARIANT == 30 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh30_gradvec.hh"
#elif MSH_VARIANT == 31 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh31_gradvec.hh"
#elif MSH_VARIANT == 32 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh32_gradvec.hh"
#elif MSH_VARIANT == 33 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh33_gradvec.hh"
#elif MSH_VARIANT == 34 && GRADVEC == 1
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh34_gradvec.hh"
#else
#include "sumfact_poisson_fastdg_3d_facedir_facemod_variation_localoperator_msh35_gradvec.hh"
#endif


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


int main(int argc, char** argv){
  try
  {
    std::cout << "Build fastdg test for MSH_VARIANT: " << MSH_VARIANT << std::endl;

    // Initialize basic stuff...
    Dune::MPIHelper& mpihelper = Dune::MPIHelper::instance(argc, argv);
    using RangeType = double;
    Dune::ParameterTree initree;
    Dune::ParameterTreeParser::readINITree(argv[1], initree);

    // Setup grid (view)...
    using Grid = Dune::UGGrid<3>;
    using GV = Grid::LeafGridView;
    using DF = Grid::ctype;
    IniGridFactory<Grid> factory(initree);
    std::shared_ptr<Grid> grid_nonconsistent = factory.getGrid();
    std::shared_ptr<Grid> grid = createConsistentGrid(grid_nonconsistent);
    GV gv = grid->leafGridView();

    // Set up finite element maps...
    using DG1_FEM = Dune::PDELab::QkDGLocalFiniteElementMap<DF, RangeType, 1, 3>;
    DG1_FEM dg1_fem;

    // Set up grid function spaces...
    using VectorBackendDG1 = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::fixed, Dune::QkStuff::QkSize<1, 3>::value>;
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
    using LOP_R = CLASSNAME<DG1_GFS, DG1_GFS>;
    using MatrixBackend = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
    using GO_r = Dune::PDELab::FastDGGridOperator<DG1_GFS, DG1_GFS, LOP_R, MatrixBackend, DF, RangeType, RangeType, DG1_GFS_CC, DG1_GFS_CC>;
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
    // slp.apply();

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

      V_R r(x_r);
      r=0.0;
      go_r.residual(x_s, r);
      Dune::printvector(std::cout, native(r), "residual vector", "row");




      // native(r).blubber();
      // std::cout.precision(17);
      std::vector<RangeType> residual(16);
      std::size_t i = 0;
      for (auto v : r){
        residual[i] = v;
        i++;
      }
      // for (std::size_t i=0; i<16; ++i){
      //   residual[i] = r[i];
      // }
      std::cout << "residual:" << std::endl;
      for (std::size_t i=0; i<16; ++i){
        std::cout << residual[i] << ", ";
      }
      std::cout << std::endl;

      // One 'correct' numerical solution for unstructured grid
      std::vector<RangeType> solution {-0.057104007824202004, -0.0024731701973568316, -0.046356852559280147, -0.0027796990290359386, -0.059846762373056507, -0.0018692117846729277, -0.059392343130923175, -0.001819348168293539, 0.0045404278062097974, 0.058001699047809038, 0.003253630695976081, 0.053457041807397923, 0.0029356233595935395, 0.055070262236853566, 0.0022382207545877291, 0.052144489358393387};

      std::cout << "is_permuation: "
                << fuzzy_is_permutation(solution, residual) << std::endl;
      if (!fuzzy_is_permutation(solution, residual)){
        return 1;
      }


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
