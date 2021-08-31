#ifndef DUNE_ALUGRID_CAPABILITIES_HH
#define DUNE_ALUGRID_CAPABILITIES_HH

#include <dune/common/version.hh>
#include <dune/geometry/type.hh>
#include <dune/grid/common/capabilities.hh>
#include <dune/alugrid/common/declaration.hh>

/** @file
 *  @author Robert Kloefkorn
 *  @brief Capabilities for ALUGrid
 */

namespace Dune
{

  namespace Capabilities
  {

    // Capabilities for ALUGrid
    // ------------------------

    /** \brief ALUGrid has only one geometry type for codim 0 entities
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, class Comm >
    struct hasSingleGeometryType< ALUGrid< dim, dimworld, eltype, refinementtype, Comm > >
    {
      static const bool v = true;
      static const unsigned int topologyId = (eltype == cube) ?
        Impl :: CubeTopology< dim > :: type :: id :
        Impl :: SimplexTopology< dim > :: type :: id ;
    };

    /** \brief ALUGrid has entities for all codimension
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, class Comm, int cdim >
    struct hasEntity< ALUGrid< dim, dimworld, eltype, refinementtype, Comm >, cdim >
    {
      static const bool v = true;
    };

    /** \brief ALUGrid can communicate when Comm == ALUGridMPIComm
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, int codim >
    struct canCommunicate< ALUGrid< dim, dimworld, eltype, refinementtype, ALUGridNoComm >, codim >
    {
      static const bool v = false;
    };

    /** \brief ALUGrid can communicate
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, int codim >
    struct canCommunicate< ALUGrid< dim, dimworld, eltype, refinementtype, ALUGridMPIComm >, codim >
    {
      static const bool v = true;
    };

    /** \brief ALUGrid has conforming level grids
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, class Comm >
    struct isLevelwiseConforming< ALUGrid< dim, dimworld, eltype, refinementtype, Comm > >
    {
      static const bool v = refinementtype == nonconforming;
    };

    /** \brief ALUGrid has conforming level grids
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, class Comm >
    struct isLeafwiseConforming< ALUGrid< dim, dimworld, eltype, refinementtype, Comm > >
    {
      static const bool v = refinementtype == conforming ;
    };

    /** \brief ALUGrid has backup and restore facilities
    \ingroup ALUGrid
    */
    template< int dim, int dimworld, ALUGridElementType eltype, ALUGridRefinementType refinementtype, class Comm >
    struct hasBackupRestoreFacilities< ALUGrid< dim, dimworld, eltype, refinementtype, Comm > >
    {
      static const bool v = true;
    };

  } // end namespace Capabilities

} //end  namespace Dune

#endif // #ifdef DUNE_ALUGRID_CAPABILITIES_HH