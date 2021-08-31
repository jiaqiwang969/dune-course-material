// -*- tab-width: 2; indent-tabs-mode: nil -*-
#ifdef HAVE_CONFIG_H
#include "config.h"
#endif
#include <iostream>
#include <vector>
#include <map>
#include <string>
#include <random>
#include <dune/common/parallel/mpihelper.hh>
#include <dune/common/exceptions.hh>
#include <dune/common/fvector.hh>
#include <dune/grid/yaspgrid.hh>
#include <dune/grid/io/file/vtk/subsamplingvtkwriter.hh>
#include <dune/istl/bvector.hh>
#include <dune/istl/operators.hh>
#include <dune/istl/solvers.hh>
#include <dune/istl/preconditioners.hh>
#include <dune/istl/io.hh>

#include <dune/pdelab/common/function.hh>
#include <dune/pdelab/common/functionutilities.hh>
#include <dune/pdelab/finiteelementmap/qkdg.hh>
#include <dune/pdelab/gridfunctionspace/gridfunctionspaceutilities.hh>
#include <dune/pdelab/gridfunctionspace/subspace.hh>
#include <dune/pdelab/gridfunctionspace/vectorgridfunctionspace.hh>
#include <dune/pdelab/gridfunctionspace/vtk.hh>
#include <dune/pdelab/gridoperator/gridoperator.hh>
#include <dune/pdelab/gridfunctionspace/interpolate.hh>
#include <dune/pdelab/localoperator/dgnavierstokes.hh>
#include <dune/pdelab/backend/istl.hh>
#include <dune/pdelab/finiteelementmap/monomfem.hh>
#include <dune/pdelab/common/function.hh>
#include <dune/pdelab/common/vtkexport.hh>
#include <dune/pdelab/constraints/p0.hh>
#include<dune/pdelab/gridoperator/onestep.hh>
#include<dune/pdelab/newton/newton.hh>
#include "dune/codegen/vtkpredicate.hh"
#include "dune/grid/io/file/vtk/vtksequencewriter.hh"

#include "taylor-green.hh"


#define PERIODIC
// #define NORMALIZE_PRESSURE

//===============================================================
// Problem setup and solution
//===============================================================
template<typename GV, typename RF, int vOrder, int pOrder>
void taylor_green (const GV& gv, const Dune::ParameterTree& configuration, std::string filename)
{
  // Some types
  using ES = Dune::PDELab::AllEntitySet<GV>;
  ES es(gv);
  using DF = typename ES::Grid::ctype;
  static const unsigned int dim = ES::dimension;
  Dune::Timer timer;

  // Create finite element maps
  const int velocity_degree = 2;
  const int pressure_degree = 1;
  using FEM_V = Dune::PDELab::QkDGLocalFiniteElementMap<DF, RF, velocity_degree, dim>;
  using FEM_P = Dune::PDELab::QkDGLocalFiniteElementMap<DF, RF, pressure_degree, dim>;
  FEM_V fem_v;
  FEM_P fem_p;

  // Do not block anything and order it lexicographic
  using VectorBackend_V = Dune::PDELab::istl::VectorBackend<Dune::PDELab::istl::Blocking::none>;
  using VectorBackend_P = Dune::PDELab::istl::VectorBackend<Dune::PDELab::istl::Blocking::none>;
  using VectorBackend = Dune::PDELab::istl::VectorBackend<Dune::PDELab::istl::Blocking::none>;
  using OrderingTag_V = Dune::PDELab::LexicographicOrderingTag;

  // For periodic boundary conditions in Yasp grid we need an
  // overlap. Therefore we run our program in parallel and need these
  // constraints
#ifdef PERIODIC
  using Con = Dune::PDELab::P0ParallelConstraints;
#else
  using Con = Dune::PDELab::NoConstraints;
#endif

  // Velocity GFS
  using GFS_V = Dune::PDELab::VectorGridFunctionSpace<
    ES,FEM_V,dim,
    VectorBackend,
    VectorBackend_V,
    Con,
    OrderingTag_V
    >;
  GFS_V gfs_v(es,fem_v);
  gfs_v.name("v");

  // Pressure GFS
  using GFS_P = Dune::PDELab::GridFunctionSpace<
    ES,
    FEM_P,
    Con,
    VectorBackend_P>;
  GFS_P gfs_p(es,fem_p);
  gfs_p.name("p");


  // GFS
  using OrderingTag = Dune::PDELab::LexicographicOrderingTag;
  using GFS = Dune::PDELab::CompositeGridFunctionSpace<VectorBackend,OrderingTag,GFS_V,GFS_P>;
  GFS gfs(gfs_v, gfs_p);
  using namespace Dune::Indices;
  gfs_v.child(_0).name("velocity_0");
  gfs_v.child(_1).name("velocity_1");
  gfs_p.name("pressure");
  gfs.name("test");
  gfs.update();
  using CC = typename GFS::template ConstraintsContainer<double>::Type;
  CC cc;
  cc.clear();
#ifdef PERIODIC
  Dune::PDELab::constraints(gfs,cc);
#endif
  std::cout << "gfs with " << gfs.size() << " dofs generated  "<< std::endl;
  std::cout << "cc with " << cc.size() << " dofs generated  "<< std::endl;

  // Parameter functions
  using FType = ZeroVectorFunction<ES,RF,dim>;
  FType f(es);
  using BType = BCTypeParamGlobalDirichlet;
  BType b;
  using VType = TaylorGreenVelocity<ES,RF,dim>;
  VType v(es, configuration.sub("parameters"));
  using PType = TaylorGreenPressure<ES,RF>;
  PType p(es, configuration.sub("parameters"));
  using PenaltyTerm = Dune::PDELab::DefaultInteriorPenalty<RF>;

  // Local operator
  using LOP_Parameters =
    Dune::PDELab::DGNavierStokesParameters<ES,RF,FType,BType,VType,PType,true,false,PenaltyTerm>;
  LOP_Parameters lop_parameters(configuration.sub("parameters"),f,b,v,p);
  using LOP = Dune::PDELab::DGNavierStokes<LOP_Parameters>;
  const int superintegration_order = 0;
  LOP lop(lop_parameters,superintegration_order);
  using LOP_M = Dune::PDELab::NavierStokesMass<LOP_Parameters>;
  LOP_M lop_m(lop_parameters,1);

  // Grid operator
  using MBE = Dune::PDELab::istl::BCRSMatrixBackend<>;
  MBE mbe(75); // Maximal number of nonzeroes per row can be cross-checked by patternStatistics().
  using GO_R = Dune::PDELab::GridOperator<GFS,GFS,LOP,MBE,RF,RF,RF,CC,CC>;
  GO_R go_r(gfs,cc,gfs,cc,lop,mbe);
  using GO_M = Dune::PDELab::GridOperator<GFS,GFS,LOP_M,MBE,RF,RF,RF,CC,CC>;
  GO_M go_m(gfs,cc,gfs,cc,lop_m,mbe);
  using IGO = Dune::PDELab::OneStepGridOperator<GO_R,GO_M>;
  IGO igo(go_r,go_m);

  // Create initial solution
  using InitialVelocity = TaylorGreenVelocity<GV,RF,2>;
  InitialVelocity initial_velocity(gv, configuration.sub("parameters"));
  using InitialPressure = TaylorGreenPressure<GV,RF>;
  InitialPressure initial_pressure(gv, configuration.sub("parameters"));
  using InitialSolution = Dune::PDELab::CompositeGridFunction<InitialVelocity,InitialPressure>;
  InitialSolution initial_solution(initial_velocity, initial_pressure);

  // Make coefficent vector and initialize it from a function
  using V = typename IGO::Traits::Domain;
  V xold(gfs);
  xold = 0.0;
  Dune::PDELab::interpolate(initial_solution,gfs,xold);

  // Solver
#ifdef PERIODIC
  using LinearSolver = Dune::PDELab::ISTLBackend_OVLP_BCGS_ILU0<GFS,CC>;
  LinearSolver ls(gfs,cc);
#else
  using LinearSolver = Dune::PDELab::ISTLBackend_SEQ_BCGS_ILU0;
  LinearSolver ls;
  // using LinearSolver = Dune::PDELab::ISTLBackend_SEQ_UMFPack;
  // LinearSolver ls(false);
#endif
  using PDESolver = Dune::PDELab::Newton<IGO,LinearSolver,V>;
  PDESolver newton(igo,xold,ls);
  // newton.setReassembleThreshold(0.0);
  // newton.setVerbosityLevel(2);
  // newton.setMaxIterations(50);
  // newton.setLineSearchMaxIterations(30);

  // Time stepping
  // using TSM = Dune::PDELab::OneStepThetaParameter<RF>;
  // TSM tsm(1.0);
  using TSM = Dune::PDELab::Alexander2Parameter<RF>;
  TSM tsm;
  Dune::PDELab::OneStepMethod<RF,IGO,PDESolver,V,V> osm(tsm,igo,newton);
  // osm.setVerbosityLevel(2);

  // Set time
  RF time = 0.0;
  RF time_end = configuration.get<RF>("driver.time_end");
  RF dt = configuration.get<RF>("driver.dt");
  RF dt_min = 1e-8;

  // Visualize initial condition
  using VTKSW = Dune::VTKSequenceWriter<GV>;
  using VTKWriter = Dune::SubsamplingVTKWriter<GV>;
  VTKWriter vtkwriter(gv, 2);
  VTKSW vtkSequenceWriter(std::make_shared<VTKWriter>(vtkwriter), filename);
  CuttingPredicate predicate;
  Dune::PDELab::addSolutionToVTKWriter(vtkSequenceWriter, gfs, xold, Dune::PDELab::vtk::defaultNameScheme(), predicate);
  vtkSequenceWriter.write(time, Dune::VTK::appendedraw);

  V x(gfs,0.0);

#ifdef NORMALIZE_PRESSURE
  // Pressure normalization
  using PressureSubGFS = typename Dune::PDELab::GridFunctionSubSpace <GFS,Dune::TypeTree::TreePath<1> >;
  PressureSubGFS pressureSubGfs(gfs);
  using PDGF = Dune::PDELab::DiscreteGridFunction<PressureSubGFS,V>;
  PDGF pdgf(pressureSubGfs,x);
  typename PDGF::Traits::RangeType pressure_integral(0);

  int elements = int(sqrt(gv.size(0)));
  int pressure_index = elements * elements * dim * pow((velocity_degree + 1), dim);
  using Dune::PDELab::Backend::native;
  std::cout << std::endl;
  std::cout << "info elements: " << elements << std::endl;
  std::cout << "info pressure_index: " << pressure_index << std::endl;
  std::cout << "info gfs.size(): " << gfs.size() << std::endl;
  std::cout << "info native(x).size(): " << native(x).size() << std::endl;
  std::cout << std::endl;
#endif

  // Time loop
  int step = 0;
  const int nth = configuration.get<RF>("driver.nth");
  while (time < time_end - dt_min*0.5){
    osm.apply(time,dt,xold,x);

#ifdef NORMALIZE_PRESSURE
    // Correct pressure after each step. Without this pressure
    // correction the velocity will be ok but the pressure will be
    // shifted by a constant.
    Dune::PDELab::integrateGridFunction(pdgf,pressure_integral,2);
    pressure_integral = gv.comm().sum(pressure_integral);
    std::cout << gv.comm().rank() << " pressure_integral before normalization: " << pressure_integral << std::endl;

    // Scale integral
    pressure_integral = pressure_integral/4;
    for (int i=pressure_index; i<gfs.size(); ++i){
      native(x)[i] -= pressure_integral;
    }
    Dune::PDELab::integrateGridFunction(pdgf,pressure_integral,2);
    pressure_integral = gv.comm().sum(pressure_integral);
    std::cout << "pressure_integral after normalization: " << pressure_integral << std::endl;
#endif

    xold = x;
    time += dt;
    step++;

    if(step%nth==0){
      vtkSequenceWriter.write(time, Dune::VTK::appendedraw);
    }
  }
}

//===============================================================
// Main program with grid setup
//===============================================================
int main(int argc, char** argv)
{
  try{
    // Maybe initialize Mpi
    Dune::MPIHelper::instance(argc, argv);

    // Read ini file
    Dune::ParameterTree configuration;
    const std::string config_filename("taylor-green.ini");
    std::cout << "Reading ini-file \""<< config_filename
              << "\"" << std::endl;
    Dune::ParameterTreeParser::readINITree(config_filename, configuration);

    // Create grid
    const int dim = 2;
    const int cells_per_dir = configuration.get<double>("driver.cells_per_dir");
    Dune::FieldVector<double,dim> lowerleft(-1.0);
    Dune::FieldVector<double,dim> upperright(1.0);
    std::array<int, dim> cells(Dune::fill_array<int, dim>(cells_per_dir));
    std::bitset<dim> periodic(false);
    int overlap = 0;
#ifdef PERIODIC
    periodic[0] = true;
    periodic[1] = true;
    overlap = 1;
#endif
    using Grid = Dune::YaspGrid<dim, Dune::EquidistantOffsetCoordinates<double, dim> >;
    Grid grid(lowerleft, upperright, cells, periodic, overlap);

    // Solve problem
    using GV = Grid::LeafGridView;
    const GV gv=grid.leafGridView();
    Dune::dinfo.push(false);
    taylor_green<GV,double,2,1>(gv,configuration,"taylor-green");
    return 0;
  }
  catch (Dune::Exception &e){
    std::cerr << "Dune reported error: " << e << std::endl;
    return 1;
  }
  catch (...){
    std::cerr << "Unknown exception thrown!" << std::endl;
    return 1;
  }
}
