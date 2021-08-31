// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_SCHUR_LOP_HH
#define DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_SCHUR_LOP_HH


#include "dune/localfunctions/lagrange/lagrangecube.hh"
#include <dune/istl/ldl.hh>
#include <dune/pdelab/finiteelement/localbasiscache.hh>
#include <dune/istl/solver.hh>
#include <dune/istl/io.hh>
#include "dune/pdelab/gridfunctionspace/gridfunctionspace.hh"
#include "dune/pdelab/localoperator/idefault.hh"
#include "dune/pdelab/localoperator/flags.hh"
#include "dune/pdelab/localoperator/pattern.hh"
#include "dune/pdelab/finiteelement/localbasiscache.hh"
#include "dune/pdelab/common/quadraturerules.hh"
#include "dune/pdelab/localoperator/defaultimp.hh"
#include "localvectorview.hh"


template<typename LOP, typename LocalDecomposition, int k>
struct SchurWrapper {

  SchurWrapper(LOP& lop_, std::shared_ptr<const LocalDecomposition> p_decomp_)
      : lop(lop_), p_decomp(p_decomp_){ }

  template<typename EG, typename X, typename Y, typename LFSU, typename LFSV>
  void interface_apply(const EG &eg, const LFSU& lfsu, const X &x, const LFSV& lfsv, Y &y) const {
    static X x_loc(x);
    static Y y_loc(y);
    x_loc = 0.;
    y_loc = 0.;

    p_decomp->copy_interface(eg, x, x_loc);

    auto y_view = LocalVectorView(y_loc);
    lop.jacobian_apply_volume(eg, lfsu, LocalVectorView(x_loc), lfsv, y_view);

    y = 0.;
    p_decomp->copy_interface(eg, y_loc, y);
  }

  template<typename EG, typename X, typename Y, typename LFSU, typename LFSV>
  void interface_cell_apply(const EG &eg, const LFSU& lfsu, const X &x, const LFSV& lfsv, Y &y) const {
    static X x_loc(x);
    static Y y_loc(y);
    static const auto zero = create_zero(x);
    x_loc = 0.;
    y_loc = 0.;

    p_decomp->copy_cell(eg, x, x_loc);

    auto y_view = LocalVectorView(y_loc);
    lop.jacobian_apply_volume(eg, lfsu, LocalVectorView(x_loc), lfsv, y_view);

    y = 0.;
    p_decomp->copy_interface(eg, y_loc, y);
  }

  template<typename EG, typename X, typename Y, typename LFSU, typename LFSV>
  void cell_interface_apply(const EG &eg, const LFSU& lfsu, const X &x, const LFSV& lfsv, Y &y) const {
    static X x_loc(x);
    static Y y_loc(y);
    static const auto zero = create_zero(x);
    x_loc = 0.;
    y_loc = 0.;

    p_decomp->copy_interface(eg, x, x_loc);

    auto y_view = LocalVectorView(y_loc);
    lop.jacobian_apply_volume(eg, lfsu, LocalVectorView(x_loc), lfsv, y_view);

    y = 0;
    p_decomp->copy_cell(eg, y_loc, y);
  }

private:
  LOP& lop;
  std::shared_ptr<const LocalDecomposition> p_decomp = {};
};

#endif //DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_SCHUR_LOP_HH
