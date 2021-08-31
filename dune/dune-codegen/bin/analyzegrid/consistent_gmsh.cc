#include "config.h"

#include <iostream>
#include <iomanip>
#include <dune/common/parallel/mpihelper.hh>
#include <dune/grid/uggrid.hh>
#include <dune/grid/io/file/gmshreader.hh>

#include <dune/consistent-edge-orientation/createconsistentgrid.hh>

int main(int argc, char** argv){
   try
   {
    if (argc != 3){
      std::cout << "Need input gmsh file and output filename." << std::endl;
      return 1;
    }

    // Initialize basic stuff...
    Dune::MPIHelper& mpihelper = Dune::MPIHelper::instance(argc, argv);
    using RangeType = double;
    std::string infile = std::string(argv[1]);

    // From the ini file we can't extract if the grid is a 2D or a 3D grid. We
    // just try the 3D case. If the msh file is a 2D grid Dune will throw an
    // error and we do the 2D version below. Not pretty but it works.
    try{
      // Setup grid (view)...
      const int dim = 3;
      using Grid = Dune::UGGrid<dim>;
      using GV = Grid::LeafGridView;
      auto grid = Dune::GmshReader<Grid>::read(infile);
      GV gv = grid->leafGridView();

      std::string filename = std::string(argv[2]);
      createConsistentGmshFile(gv, filename);
    }
    catch(Dune::Exception &e){
      // Setup grid (view)...
      const int dim = 2;
      using Grid = Dune::UGGrid<dim>;
      using GV = Grid::LeafGridView;
      auto grid = Dune::GmshReader<Grid>::read(infile);
      GV gv = grid->leafGridView();

      std::string filename = std::string(argv[2]);
      createConsistentGmshFile(gv, filename);
    }
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
