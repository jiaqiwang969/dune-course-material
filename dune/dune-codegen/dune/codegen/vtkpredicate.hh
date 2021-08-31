#ifndef DUNE_CODEGEN_VTKPREDICATE_HH
#define DUNE_CODEGEN_VTKPREDICATE_HH

#include <dune/typetree/nodeinterface.hh>

/** A predicate for vtk output
 *  that cuts all vector grid function spaces with a length greater than 4.
 *  This is necessary because VTK cannot handle them.
 */
struct CuttingPredicate
{
  template<typename T, typename TP>
  bool operator()(const T& t, TP tp) const
  {
    return Dune::TypeTree::degree(t) < 4;
  }
};

#endif
