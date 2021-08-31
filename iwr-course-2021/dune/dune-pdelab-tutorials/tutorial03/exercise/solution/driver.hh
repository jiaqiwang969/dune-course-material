/********************************************************/
// Beware of line number changes, they may corrupt docu!
//! \brief Driver function to set up and solve the problem
/********************************************************/

template<typename GV, typename FEM>
void driver (const GV& gv, const FEM& fem, Dune::ParameterTree& ptree)
{
  // dimension and important types
  const int dim = GV::dimension;
  typedef double RF;                   // type for computations

  // make user functions and set initial time
  RF time = 0.0;
  RF eta = ptree.get("problem.eta",(RF)1.0);
  Problem<RF> problem(eta);
  problem.setTime(time);
  auto glambda = [&](const auto& e, const auto& x)
    {return problem.g(e,x);};
  auto g = Dune::PDELab::
    makeInstationaryGridFunctionFromCallable(gv,glambda,problem);
  auto blambda = [&](const auto& i, const auto& x)
    {return problem.b(i,x);};
  auto b = Dune::PDELab::
    makeBoundaryConditionFromCallable(gv,blambda);

  // Make grid function space
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

  // initialize simulation time,  the coefficient vector
  Dune::PDELab::interpolate(g,gfs,z);

  // Make instationary grid operator
  typedef NonlinearHeatFEM<Problem<RF>,FEM> LOP;
  LOP lop(problem);
  typedef Dune::PDELab::ISTL::BCRSMatrixBackend<> MBE;
  int degree = ptree.get("fem.degree",(int)1);
  MBE mbe((int)pow(1+2*degree,dim));
  typedef Dune::PDELab::GridOperator<GFS,GFS,LOP,MBE,
                                     RF,RF,RF,CC,CC> GO0;
  GO0 go0(gfs,cc,gfs,cc,lop,mbe);
  typedef L2<FEM> TLOP;
  TLOP tlop;
  typedef Dune::PDELab::GridOperator<GFS,GFS,TLOP,MBE,
                                     RF,RF,RF,CC,CC> GO1;
  GO1 go1(gfs,cc,gfs,cc,tlop,mbe);
  typedef Dune::PDELab::OneStepGridOperator<GO0,GO1> IGO;
  IGO igo(go0,go1);

  // Select a linear solver backend
  typedef Dune::PDELab::ISTLBackend_SEQ_CG_AMG_SSOR<IGO> LS;
  LS ls(100,0);

  // solve nonlinear problem
  typedef Dune::PDELab::StationaryLinearProblemSolver<IGO,LS,Z> PDESOLVER;
  PDESOLVER pdesolver(igo,ls,z,1e-10);

  // select and prepare time-stepping scheme
  // Dune::PDELab::Alexander2Parameter<RF> pmethod;
  // Dune::PDELab::ImplicitEulerParameter<RF> pmethod;
  // Dune::PDELab::OneStepThetaParameter<RF> pmethod(0.5);
  Dune::PDELab::FractionalStepParameter<RF> pmethod;

  typedef Dune::PDELab::OneStepMethod<RF,IGO,PDESOLVER,Z,Z> OSM;
  OSM osm(pmethod,igo,pdesolver);
  osm.setVerbosityLevel(2);

  // prepare VTK writer and write first file
  std::string filename=ptree.get("output.filename","output");
  struct stat st;
  if( stat( filename.c_str(), &st ) != 0 )
    {
      int stat = 0;
      stat = mkdir(filename.c_str(),S_IRWXU|S_IRWXG|S_IRWXO);
      if( stat != 0 && stat != -1)
        std::cout << "Error: Cannot create directory "
                  << filename << std::endl;
    }
  int subsampling=ptree.get("output.subsampling",(int)1);
  typedef Dune::SubsamplingVTKWriter<GV> VTKWRITER;
  VTKWRITER vtkwriter(gv,Dune::refinementIntervals(subsampling));
  typedef Dune::VTKSequenceWriter<GV> VTKSEQUENCEWRITER;
  VTKSEQUENCEWRITER vtkSequenceWriter(
    std::make_shared<VTKWRITER>(vtkwriter),filename,filename,"");
  typedef Dune::PDELab::VTKGridFunctionAdapter<ZDGF> VTKF;
  vtkSequenceWriter.addVertexData(std::shared_ptr<VTKF>(
                             new VTKF(zdgf,"solution")));
  vtkSequenceWriter.write(time,Dune::VTK::appendedraw);

  // time loop
  RF T = ptree.get("problem.T",(RF)1.0);
  RF dt = ptree.get("fem.dt",(RF)0.1);
  while (time<T-1e-8)
    {
      // assemble constraints for new time step
      problem.setTime(time+dt);
      Dune::PDELab::constraints(b,gfs,cc);

      // do time step
      Z znew(z);
      osm.apply(time,dt,z,g,znew);

      // accept time step
      z = znew;
      time+=dt;

      // output to VTK file
      vtkSequenceWriter.write(time,Dune::VTK::appendedraw);
    }
}
