#include "config.h"

#include "dune/common/parallel/mpihelper.hh"
#include "dune/pdelab/stationary/linearproblem.hh"
#include "dune/pdelab/backend/istl.hh"
#include "dune/grid/yaspgrid.hh"
#include "dune/pdelab/finiteelementmap/qkdg.hh"
#include "dune/pdelab/gridoperator/fastdg.hh"
#include "dune/testtools/gridconstruction.hh"
#include "dune/common/parametertree.hh"
#include "dune/common/parametertreeparser.hh"
#include <random>
#include "dune/pdelab/gridfunctionspace/vtk.hh"
#include "dune/grid/io/file/vtk/subsamplingvtkwriter.hh"
#include "string"
#include "dune/codegen/vtkpredicate.hh"

// Include all the generated operators
#include "full_3d_operator.hh"
#include "block_diagonal_3d_operator.hh"
#include "block_offdiagonal_3d_operator.hh"
#include "point_diagonal_3d_operator.hh"

int main(int argc, char** argv){  
  try
  {    
    // Initialize basic stuff...    
    Dune::MPIHelper& mpihelper = Dune::MPIHelper::instance(argc, argv);
    using RangeType = double;
    Dune::ParameterTree initree;
    Dune::ParameterTreeParser::readINITree(argv[1], initree);
    
    // Setup grid (view)...    
    using Grid = Dune::YaspGrid<3, Dune::EquidistantCoordinates<RangeType, 3>>;
    using GV = Grid::LeafGridView;
    using DF = Grid::ctype;
    IniGridFactory<Grid> factory(initree);
    std::shared_ptr<Grid> grid = factory.getGrid();
    GV gv = grid->leafGridView();
    
    // Set up finite element maps...    
    using DG2_FEM = Dune::PDELab::QkDGLocalFiniteElementMap<DF, RangeType, 1, 3>;
    DG2_FEM dg2_fem;
    
    // Set up grid function spaces...    
    using VectorBackendDG2 = Dune::PDELab::ISTL::VectorBackend<Dune::PDELab::ISTL::Blocking::fixed>;
    using NoConstraintsAssembler = Dune::PDELab::NoConstraints;
    using DG2_GFS = Dune::PDELab::GridFunctionSpace<GV, DG2_FEM, NoConstraintsAssembler, VectorBackendDG2>;
    DG2_GFS dg2_gfs_(gv, dg2_fem);
    dg2_gfs_.name("dg2_gfs_");
    
    // Set up constraints container...    
    using DG2_GFS_CC = DG2_GFS::ConstraintsContainer<RangeType>::Type;
    DG2_GFS_CC dg2_gfs__cc;
    dg2_gfs__cc.clear();
    Dune::PDELab::constraints(dg2_gfs_, dg2_gfs__cc);
    
    // Set up grid grid operators...    
    using FullLOP = FullOperator<DG2_GFS, DG2_GFS>;
    using MatrixBackend = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
    using FullGO = Dune::PDELab::FastDGGridOperator<DG2_GFS, DG2_GFS, FullLOP, MatrixBackend, DF, RangeType, RangeType, DG2_GFS_CC, DG2_GFS_CC>;
    FullLOP fulllop(dg2_gfs_, dg2_gfs_, initree);
    dg2_gfs_.update();
    MatrixBackend mb(5);
    FullGO fullgo(dg2_gfs_, dg2_gfs__cc, dg2_gfs_, dg2_gfs__cc, fulllop, mb);

    // Additional grid operators for preconditioner
    using BDLOP = BlockDiagonalOperator<DG2_GFS, DG2_GFS>;
    using BDGO = Dune::PDELab::FastDGGridOperator<DG2_GFS, DG2_GFS, BDLOP, MatrixBackend, DF, RangeType, RangeType, DG2_GFS_CC, DG2_GFS_CC>;
    BDLOP bdlop(dg2_gfs_, dg2_gfs_, initree);
    BDGO bdgo(dg2_gfs_, dg2_gfs__cc, dg2_gfs_, dg2_gfs__cc, bdlop, mb);

    using BODLOP = BlockOffDiagonalOperator<DG2_GFS, DG2_GFS>;
    using BODGO = Dune::PDELab::FastDGGridOperator<DG2_GFS, DG2_GFS, BODLOP, MatrixBackend, DF, RangeType, RangeType, DG2_GFS_CC, DG2_GFS_CC>;
    BODLOP bodlop(dg2_gfs_, dg2_gfs_, initree);
    BODGO bodgo(dg2_gfs_, dg2_gfs__cc, dg2_gfs_, dg2_gfs__cc, bodlop, mb);

    using PDLOP = PointDiagonalOperator<DG2_GFS, DG2_GFS>;
    using PDGO = Dune::PDELab::FastDGGridOperator<DG2_GFS, DG2_GFS, PDLOP, MatrixBackend, DF, RangeType, RangeType, DG2_GFS_CC, DG2_GFS_CC>;
    PDLOP pdlop(dg2_gfs_, dg2_gfs_, initree);
    PDGO pdgo(dg2_gfs_, dg2_gfs__cc, dg2_gfs_, dg2_gfs__cc, pdlop, mb);

    // Set up solution vectors...    
    using V_R = Dune::PDELab::Backend::Vector<DG2_GFS,DF>;
    V_R x(dg2_gfs_, 0.0);
    
    // Testing!
    
    // Assemble all those matrices
    using Dune::PDELab::Backend::native;
    using M = typename FullGO::Traits::Jacobian;
    M m(fullgo);
    fullgo.jacobian(x, m);
    Dune::printmatrix(std::cout, native(m),"full matrix","row",9,1);

    using BDM = typename BDGO::Traits::Jacobian;
    BDM bdm(bdgo);
    bdgo.jacobian(x, bdm);
    Dune::printmatrix(std::cout, native(bdm),"blockdiagonal matrix","row",9,1);

    using BODM = typename BODGO::Traits::Jacobian;
    BODM bodm(bodgo);
    bodgo.jacobian(x, bodm);
    Dune::printmatrix(std::cout, native(bodm),"blockoffdiagonal matrix","row",9,1);

    V_R pd(dg2_gfs_, 0.0);
    pdgo.residual(x, pd);
    Dune::printvector(std::cout, native(pd), "point diagonal vector", "row");

    // test failure boolean
    bool testfail(false);

    // TODO: Properly test this stuff given the above matrices.
    //       Right now, visuals need to suffice.

    // Return statement...    
    return testfail;
    
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

