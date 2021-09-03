#ifndef DUNE_PERFTOOL_TEST_NONLINEAR_REFERENCE_DRIVER_HH
#define DUNE_PERFTOOL_TEST_NONLINEAR_REFERENCE_DRIVER_HH

#include <dune/common/parametertreeparser.hh>
#include <dune/pdelab/constraints/conforming.hh>
#include <dune/pdelab/finiteelementmap/pkfem.hh>
#include <dune/grid/io/file/vtk/subsamplingvtkwriter.hh>
#include <dune/alugrid/grid.hh>
#include <dune/pdelab/backend/istl.hh>
#include <dune/pdelab/function/callableadapter.hh>
#include <dune/testtools/gridconstruction.hh>
#include <dune/common/parametertree.hh>
#include <dune/pdelab/gridoperator/gridoperator.hh>
#include <dune/pdelab/gridfunctionspace/vtk.hh>
#include <dune/pdelab/newton/newton.hh>
#include <dune/codegen/vtkpredicate.hh>
#include <dune/pdelab/backend/istl.hh>
#include <string>
#include <dune/pdelab/backend/istl.hh>
#include <dune/pdelab/finiteelementmap/opbfem.hh>

#include "reference_problem.hh"
#include "reference_nonlinearpoissonfem.hh"

void driver (int argc, char** argv){
  // Dimension and important types
  const int dim = 2;
  typedef double RF;

  // Open ini file
  Dune::ParameterTree initree;
  Dune::ParameterTreeParser::readINITree(argv[1], initree);

  // Create grid
  typedef Dune::ALUGrid<dim, dim, Dune::simplex, Dune::conforming> Grid;
  IniGridFactory<Grid> factory(initree);
  std::shared_ptr<Grid> grid = factory.getGrid();
  typedef Grid::LeafGridView GV;
  GV gv = grid->leafGridView();

  // Make PDE parameter class
  RF eta = 1.0;
  Problem<RF> problem(eta);
  auto glambda = [&](const auto& e, const auto& x)
    {return problem.g(e,x);};
  auto g = Dune::PDELab::
    makeGridFunctionFromCallable(gv,glambda);
  auto blambda = [&](const auto& i, const auto& x)
    {return problem.b(i,x);};
  auto b = Dune::PDELab::
    makeBoundaryConditionFromCallable(gv,blambda);

  // Make grid function space
  typedef Grid::ctype DF;

  typedef Dune::PDELab::PkLocalFiniteElementMap<GV,DF,double,1> FEM;
  FEM fem(gv);
  typedef Dune::PDELab::ConformingDirichletConstraints CON;
  typedef Dune::PDELab::ISTL::VectorBackend<> VBE;
  typedef Dune::PDELab::GridFunctionSpace<GV,FEM,CON,VBE> GFS;
  GFS gfs(gv,fem);
  gfs.name("Vh");

  // Assemble constraints
  typedef typename GFS::template
    ConstraintsContainer<RF>::Type CC;
  CC cc;
  Dune::PDELab::constraints(b,gfs,cc); // assemble constraints
  std::cout << "constrained dofs=" << cc.size() << " of "
            << gfs.globalSize() << std::endl;

  // A coefficient vector
  using Z = Dune::PDELab::Backend::Vector<GFS,RF>;
  Z z(gfs); // initial value

  // Make a grid function out of it
  typedef Dune::PDELab::DiscreteGridFunction<GFS,Z> ZDGF;
  ZDGF zdgf(gfs,z);

  // Fill the coefficient vector
  Dune::PDELab::interpolate(g,gfs,z);

  // Make a local operator
  typedef NonlinearPoissonFEM<Problem<RF>,FEM> LOP;
  LOP lop(problem);

  // Make a global operator
  typedef Dune::PDELab::ISTL::BCRSMatrixBackend<> MBE;
  int degree = initree.get("fem.degree",(int)1);
  MBE mbe((int)pow(1+2*degree,dim));
  typedef Dune::PDELab::GridOperator<
    GFS,GFS,  /* ansatz and test space */
    LOP,      /* local operator */
    MBE,      /* matrix backend */
    RF,RF,RF, /* domain, range, jacobian field type*/
    CC,CC     /* constraints for ansatz and test space */
    > GO;
  GO go(gfs,cc,gfs,cc,lop,mbe);

  // Select a linear solver backend
  typedef Dune::PDELab::ISTLBackend_SEQ_UMFPack LS;
  LS ls(false);

  // Set up nonlinear solver
  Dune::PDELab::Newton<GO,LS,Z> newton(go,z,ls);
  // newton.setReassembleThreshold(0.0); // always reassemble J
  // newton.setVerbosityLevel(3);        // be verbose
  // newton.setReduction(1e-10);         // total reduction
  // newton.setMinLinearReduction(1e-4); // min. red. in lin. solve
  // newton.setMaxIterations(25);        // limit number of its
  // newton.setLineSearchMaxIterations(10); // limit line search

  // Solve nonlinear problem
  newton.apply();

  // Write VTK output file
  int subsampling = initree.get("vtk.subsamplinglevel",(int)0);
  Dune::SubsamplingVTKWriter<GV> vtkwriter(gv,subsampling);
  Dune::PDELab::addSolutionToVTKWriter(vtkwriter, gfs, z);
  std::string vtkfile = initree.get<std::string>("wrapper.vtkcompare.name", "output");
  vtkwriter.write(vtkfile, Dune::VTK::ascii);
}

#endif
