#include "config.h"

#include <algorithm>

#include <dune/common/parallel/mpihelper.hh>
#include <dune/common/parametertree.hh>
#include "dune/common/parametertreeparser.hh"
#include <dune/grid/uggrid.hh>
#include <dune/grid/yaspgrid.hh>
#include <dune/pdelab/gridfunctionspace/gridfunctionspace.hh>
#include <dune/testtools/gridconstruction.hh>

#include <dune/consistent-edge-orientation/createconsistentgrid.hh>

#include <dune/codegen/sumfact/analyzegrid.hh>

int main(int argc, char** argv){
  try
  {
    if (argc != 3){
      std::cout << "Need ini file and output filename." << std::endl;
      return 1;
    }

    // Initialize basic stuff...
    Dune::MPIHelper& mpihelper = Dune::MPIHelper::instance(argc, argv);
    using RangeType = double;
    Dune::ParameterTree initree;
    Dune::ParameterTreeParser::readINITree(argv[1], initree);

    bool quadrilateral = false;
    std::string elementType = initree.get("elementType", "");
    if (elementType == "quadrilateral"){
      quadrilateral = true;
    }
    quadrilateral = quadrilateral || initree.hasKey("cells");
    std::cout << "quadrilateral: " << quadrilateral << std::endl;

    bool unstructured = initree.get("formcompiler.grid_unstructured", false);
    std::cout << "unstructured: " << unstructured << std::endl;

    std::string filename = std::string(argv[2]);
    std::cout << "writing into: " << filename << std::endl;

    bool gmsh = initree.hasKey("gmshFile");

    if (gmsh){
      // From the ini file we can't extract if the grid is a 2D or a 3D
      // grid. We just try the 3D case. If the msh file is a 2D grid Dune will
      // throw an error and we do the 2D version below. Not pretty but it
      // works.
      try{
        // Setup grid (view)...
        const int dim = 3;
        using Grid = Dune::UGGrid<dim>;
        using GV = Grid::LeafGridView;
        IniGridFactory<Grid> factory(initree);
        std::shared_ptr<Grid> grid_nonconsistent = factory.getGrid();
        std::shared_ptr<Grid> grid = createConsistentGrid(grid_nonconsistent);

        GV gv = grid->leafGridView();

        // Extract facemod/facedir intersection variation
        using ES = Dune::PDELab::AllEntitySet<GV>;
        ES es(gv);
        std::cout << "Analyse 3d gmsh grid" << std::endl;
        analyze_grid(es, filename);
      }
      catch(Dune::Exception &e){
        // Setup grid (view)...
        const int dim = 2;
        using Grid = Dune::UGGrid<dim>;
        using GV = Grid::LeafGridView;
        IniGridFactory<Grid> factory(initree);
        std::shared_ptr<Grid> grid_nonconsistent = factory.getGrid();
        std::shared_ptr<Grid> grid = createConsistentGrid(grid_nonconsistent);

        GV gv = grid->leafGridView();

        // Extract facemod/facedir intersection variation
        using ES = Dune::PDELab::AllEntitySet<GV>;
        ES es(gv);
        std::cout << "Analyse 2d gmsh grid" << std::endl;
        analyze_grid(es, filename);
      }
    }
    else if (quadrilateral){
      if (unstructured){
        std::vector<int> tmp;
        std::vector<int> dim_counter = initree.get("elements", tmp);
        const int dim = dim_counter.size();
        std::cout << "dim: " << dim << std::endl;

        if (dim == 2){
          // Setup grid (view)...
          using Grid = Dune::UGGrid<2>;
          using GV = Grid::LeafGridView;
          IniGridFactory<Grid> factory(initree);
          std::shared_ptr<Grid> grid_nonconsistent = factory.getGrid();
          std::shared_ptr<Grid> grid = createConsistentGrid(grid_nonconsistent);
          GV gv = grid->leafGridView();

          // Extract facemod/facedir intersection variation
          using ES = Dune::PDELab::AllEntitySet<GV>;
          ES es(gv);
          std::cout << "Analyse 2d unstructured quadrilateral grid" << std::endl;
          analyze_grid(es, filename);
        }
        else if (dim == 3){
          // Setup grid (view)...
          using Grid = Dune::UGGrid<3>;
          using GV = Grid::LeafGridView;
          IniGridFactory<Grid> factory(initree);
          std::shared_ptr<Grid> grid_nonconsistent = factory.getGrid();
          std::shared_ptr<Grid> grid = createConsistentGrid(grid_nonconsistent);
          GV gv = grid->leafGridView();

          // Extract facemod/facedir intersection variation
          using ES = Dune::PDELab::AllEntitySet<GV>;
          ES es(gv);
          std::cout << "Analyse 3d unstructured quadrilateral grid" << std::endl;
          analyze_grid(es, filename);
        }
        else{
          assert(false);
        }
      }
      else {
        std::vector<int> tmp;
        std::vector<int> dim_counter = initree.get("cells", tmp);
        const int dim = dim_counter.size();
        std::cout << "dim: " << dim << std::endl;

        if (dim == 2){
          // For structured grids we already know the variation beforehand. This
          // is only implemented to cover all the cases.

          // Setup grid (view)...
          using Grid = Dune::YaspGrid<2>;
          using GV = Grid::LeafGridView;
          IniGridFactory<Grid> factory(initree);
          std::shared_ptr<Grid> grid = factory.getGrid();
          GV gv = grid->leafGridView();

          // Extract facemod/facedir intersection variation
          using ES = Dune::PDELab::AllEntitySet<GV>;
          ES es(gv);
          std::cout << "Analyse 2d structured quadrilateral grid" << std::endl;
          analyze_grid(es, filename);
        }
        if (dim == 3){
          // For structured grids we already know the variation beforehand. This
          // is only implemented to cover all the cases.

          // Setup grid (view)...
          using Grid = Dune::YaspGrid<3>;
          using GV = Grid::LeafGridView;
          IniGridFactory<Grid> factory(initree);
          std::shared_ptr<Grid> grid = factory.getGrid();
          GV gv = grid->leafGridView();

          // Extract facemod/facedir intersection variation
          using ES = Dune::PDELab::AllEntitySet<GV>;
          ES es(gv);
          std::cout << "Analyse 3d structured quadrilateral grid" << std::endl;
          analyze_grid(es, filename);
        }
        else{
          assert (false);
        }
      }
    }
    else{
      // We can't do sum factorization on simplicial meshes
      assert (false);
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
