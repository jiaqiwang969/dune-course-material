#ifndef DUNE_CODEGEN_BLOCKSTRUCTUREDQKFEM_HH
#define DUNE_CODEGEN_BLOCKSTRUCTUREDQKFEM_HH


#include <cstddef>

#include <dune/common/power.hh>
#include <dune/localfunctions/lagrange/qk.hh>
#include <dune/pdelab/finiteelementmap/finiteelementmap.hh>

namespace Dune {
  namespace PDELab {

    //! wrap up element from local functions
    //! \ingroup FiniteElementMap
    template<typename GV, typename D, typename R, std::size_t k>
    class BlockstructuredQkLocalFiniteElementMap
        : public SimpleLocalFiniteElementMap< Dune::QkLocalFiniteElement<D,R,GV::dimension,k>, GV::dimension>
    {

    public:

      BlockstructuredQkLocalFiniteElementMap(const GV& gv)
      {}

      bool fixedSize() const
      {
        return true;
      }

      bool hasDOFs(int codim) const
      {
        switch(k)
        {
          case 1:
            return codim == GV::dimension;
          default:
            return 1;
        }
      }

      std::size_t size(GeometryType gt) const
      {
        std::size_t acc = 1;
        for(std::size_t i = 0; i < gt.dim(); ++i)
          acc *= k-1;
        return acc;
      }

      std::size_t maxLocalSize() const
      {
        return Dune::StaticPower<k+1,GV::dimension>::power;
      }

    };

  }
}


#endif //DUNE_CODEGEN_BLOCKSTRUCTUREDQKFEM_HH
