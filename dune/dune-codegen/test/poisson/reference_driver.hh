#ifndef _HOME_DOMINIC_DUNE_BUILD_DUNE_PERFTOOL_TEST_LAPLACE_LAPLACE_DG_SYMDIFF_DRIVER_HH
#define _HOME_DOMINIC_DUNE_BUILD_DUNE_PERFTOOL_TEST_LAPLACE_LAPLACE_DG_SYMDIFF_DRIVER_HH

#include <dune/pdelab/gridoperator/gridoperator.hh>
#include <dune/pdelab/backend/istl.hh>
#include <dune/pdelab/backend/istl.hh>
#include <dune/pdelab/gridfunctionspace/vtk.hh>
#include <dune/grid/uggrid.hh>
#include <dune/pdelab/backend/istl.hh>
#include <string>
#include <dune/common/parametertree.hh>
#include <dune/pdelab/finiteelementmap/opbfem.hh>
#include <dune/grid/io/file/vtk/subsamplingvtkwriter.hh>
#include <dune/pdelab/stationary/linearproblem.hh>
#include <dune/common/parametertreeparser.hh>
#include <dune/testtools/gridconstruction.hh>
#include <dune/pdelab/localoperator/convectiondiffusiondg.hh>
#include <dune/pdelab/localoperator/convectiondiffusionparameter.hh>

template<typename GV, typename RF>
class CDProb
{
  typedef Dune::PDELab::ConvectionDiffusionBoundaryConditions::Type BCType;

  public:
  typedef Dune::PDELab::ConvectionDiffusionParameterTraits<GV,RF> Traits;

  //! tensor diffusion coefficient
  typename Traits::PermTensorType
  A (const typename Traits::ElementType& e, const typename Traits::DomainType& x) const
  {
    typename Traits::PermTensorType I;
    for (std::size_t i=0; i<Traits::dimDomain; i++)
      for (std::size_t j=0; j<Traits::dimDomain; j++)
        I[i][j] = (i==j) ? 1 : 0;
    return I;
  }

  //! velocity field
  typename Traits::RangeType
  b (const typename Traits::ElementType& e, const typename Traits::DomainType& x) const
  {
    typename Traits::RangeType v(0.0);
    return v;
  }

  //! sink term
  typename Traits::RangeFieldType
  c (const typename Traits::ElementType& e, const typename Traits::DomainType& x) const
  {
    return 0.0;
  }

  //! source term
  typename Traits::RangeFieldType
  f (const typename Traits::ElementType& e, const typename Traits::DomainType& x) const
  {
    auto global = e.geometry().global(x);
    Dune::FieldVector<double,2> c(0.5);
    c -= global;
    return 4.*(1.-c.two_norm2())*std::exp(-1.*c.two_norm2());
  }

  //! boundary condition type function
  BCType
  bctype (const typename Traits::IntersectionType& is, const typename Traits::IntersectionDomainType& x) const
  {
    return Dune::PDELab::ConvectionDiffusionBoundaryConditions::Dirichlet;
  }

  //! Dirichlet boundary condition value
  typename Traits::RangeFieldType
  g (const typename Traits::ElementType& e, const typename Traits::DomainType& x) const
  {
    auto global = e.geometry().global(x);
    Dune::FieldVector<double,2> c(0.5);
    c-= global;
    return std::exp(-1.*c.two_norm2());
  }

  //! Neumann boundary condition
  typename Traits::RangeFieldType
  j (const typename Traits::IntersectionType& is, const typename Traits::IntersectionDomainType& x) const
  {
    return 0.0;
  }

  //! outflow boundary condition
  typename Traits::RangeFieldType
  o (const typename Traits::IntersectionType& is, const typename Traits::IntersectionDomainType& x) const
  {
    return 0.0;
  }
};


void driver(int argc, char** argv){  typedef Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::none, 1> VectorBackend;
  static const int dim = 2;
  typedef Dune::UGGrid<dim> Grid;
  typedef Grid::LeafGridView GV;
  typedef Grid::ctype DF;
  typedef double R;
  typedef Dune::PDELab::OPBLocalFiniteElementMap<DF, R, 1, dim, Dune::GeometryType::simplex> DG1_FEM;
  typedef Dune::PDELab::NoConstraints NoConstraintsAssembler;
  typedef Dune::PDELab::GridFunctionSpace<GV, DG1_FEM, NoConstraintsAssembler, VectorBackend> DG1_DIRICHLET_GFS;
  Dune::ParameterTree initree;
  Dune::ParameterTreeParser::readINITree(argv[1], initree);
  IniGridFactory<Grid> factory(initree);
  std::shared_ptr<Grid> grid = factory.getGrid();
  GV gv = grid->leafGridView();
  DG1_FEM dg1_fem;
  DG1_DIRICHLET_GFS dg1_dirichlet_gfs(gv, dg1_fem);
  dg1_dirichlet_gfs.name("bla");
  typedef Dune::SubsamplingVTKWriter<GV> VTKWriter;
  int sublevel = initree.get<int>("vtk.subsamplinglevel", 0);
  VTKWriter vtkwriter(gv, sublevel);
  using LOP = Dune::PDELab::ConvectionDiffusionDG<CDProb<GV, R>, DG1_FEM>;
  typedef DG1_DIRICHLET_GFS::ConstraintsContainer<R>::Type DG1_CC;
  typedef Dune::PDELab::ISTL::BCRSMatrixBackend<> MatrixBackend;
  typedef Dune::PDELab::GridOperator<DG1_DIRICHLET_GFS, DG1_DIRICHLET_GFS, LOP, MatrixBackend, DF, R, R, DG1_CC, DG1_CC> GO;
  typedef GO::Traits::Domain V;
  V x(dg1_dirichlet_gfs);
  x = 0.0;
  std::string vtkfile = initree.get<std::string>("wrapper.vtkcompare.name", "output");
  typedef Dune::PDELab::ISTLBackend_SEQ_UMFPack LinearSolver;
  typedef Dune::PDELab::StationaryLinearProblemSolver<GO, LinearSolver, V> SLP;
  DG1_CC dg1_cc;
  dg1_cc.clear();
  CDProb<GV, R> params;
  LOP lop(params, Dune::PDELab::ConvectionDiffusionDGMethod::SIPG);
  int generic_dof_estimate =  6 * dg1_dirichlet_gfs.maxLocalSize();
  int dofestimate = initree.get<int>("istl.number_of_nnz", generic_dof_estimate);
  MatrixBackend mb(dofestimate);
  GO go(dg1_dirichlet_gfs, dg1_cc, dg1_dirichlet_gfs, dg1_cc, lop, mb);
  std::cout << "gfs with " << dg1_dirichlet_gfs.size() << " dofs generated  "<< std::endl;
  std::cout << "cc with " << dg1_cc.size() << " dofs generated  "<< std::endl;
  LinearSolver ls(false);
  double reduction = initree.get<double>("reduction", 1e-12);
  SLP slp(go, ls, x, reduction);
  slp.apply();
  Dune::PDELab::addSolutionToVTKWriter(vtkwriter, dg1_dirichlet_gfs, x);
  vtkwriter.write(vtkfile, Dune::VTK::ascii);
}

#endif //_HOME_DOMINIC_DUNE_BUILD_DUNE_PERFTOOL_TEST_LAPLACE_LAPLACE_DG_SYMDIFF_DRIVER_HH
