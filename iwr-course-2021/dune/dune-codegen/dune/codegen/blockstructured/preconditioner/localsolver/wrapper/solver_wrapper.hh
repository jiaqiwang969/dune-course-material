#ifndef NEUMANN_NEUMANN_PRECONDITIONER_SOLVER_WRAPPER_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_SOLVER_WRAPPER_HH

#include <algorithm>
#include <dune/common/reservedvector.hh>
#include <dune/grid/common/rangegenerators.hh>
#include <dune/pdelab/gridfunctionspace/localvector.hh>
#include <dune/pdelab/backend/interface.hh>
#include <dune/pdelab/common/geometrywrapper.hh>
#include "localvectorview.hh"

template<typename LOP, typename LocalDecomposition, int k>
class SolverWrapper{
public:
  explicit SolverWrapper(LOP& lop_, std::shared_ptr<const LocalDecomposition> p_decomp_)
      :lop(lop_), p_decomp(p_decomp_) { }

  template<typename EG, typename X, typename Y, typename LFSU, typename LFSV>
  void jacobian_apply_volume(const EG &eg, const LFSU& lfsu, const X &x, const LFSV& lfsv, Y &y, const bool isDirichlet,
                             const double reg) const{
    const auto x_view = LocalVectorView(x);
    auto y_view = LocalVectorView(y);

    if(isDirichlet){
      // Assumed that the element has at least one dirichlet (internal/external) face
      static const auto zero = create_zero(x);
      X z(x);

      p_decomp->copy_interface(eg, zero, z);
      auto z_view = LocalVectorView(z);
      lop.jacobian_apply_volume(eg, lfsu, z_view, lfsv, y_view);
      p_decomp->copy_interface(eg, x, y);
    } else {
      lop.jacobian_apply_volume(eg, lfsu, x_view, lfsv, y_view);
      y.axpy(reg, x);
      p_decomp->copy_exterior_boundary(eg, x, y);
    }
  }

  template<typename EG, typename X, typename Y, typename LFSU, typename LFSV>
  void jacobian_norm_estimate(const EG &eg, const LFSU& lfsu, const X &x, const LFSV& lfsv, Y &y) const{
    const auto x_view = LocalVectorView(x);
    auto y_view = LocalMatrixNormView(y);

    lop.jacobian_volume(eg, lfsu, x_view, lfsv, y_view);
  }

private:
  LOP& lop;
  std::shared_ptr<const LocalDecomposition> p_decomp = {};
};


#endif //NEUMANN_NEUMANN_PRECONDITIONER_SOLVER_WRAPPER_HH
