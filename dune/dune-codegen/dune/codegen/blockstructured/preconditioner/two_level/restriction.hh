#ifndef BLOCKSTRUCTURED_PRECONDITIONER_RESTRICTION_HH
#define BLOCKSTRUCTURED_PRECONDITIONER_RESTRICTION_HH

#include "dune/localfunctions/lagrange/lagrangecube.hh"
#include <dune/pdelab/gridoperator/gridoperator.hh>
#include <dune/pdelab/backend/istl.hh>
#include <dune/pdelab/finiteelement/localbasiscache.hh>

template<typename LOP, typename F_GFS, typename C_GFS, typename F_CC,  typename C_CC, typename Decomposition>
class RestrictionOperator{
  using DF = double;
  using RT = double;

  constexpr static int k = F_GFS::Traits::FiniteElementMap::blocks;

  using MB = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
  using GOP = Dune::PDELab::GridOperator<F_GFS, C_GFS, LOP, MB, DF, RT, RT, F_CC, C_CC>;

public:
  using F_X = typename GOP::Domain;
  using C_X = typename GOP::Range;

  RestrictionOperator(LOP& lop_, const F_GFS& f_gfs_, const F_CC& f_cc_, const C_GFS& c_gfs_, const C_CC& c_cc_,
      const Decomposition& decomp_)
      : f_gfs(f_gfs_), c_gfs(c_gfs_), f_cc(f_cc_), c_cc(c_cc_), lop(lop_),
        gop(f_gfs, f_cc, c_gfs, c_cc, lop, MB(1)), decomp(decomp_)
  {}

  const F_GFS& fine_space() const { return f_gfs;}
  const C_GFS& coarse_space() const { return c_gfs;}

  void apply(const F_X& x, C_X& y) const {
    F_X v(x);

    decomp.scale(v);

    y = 0.;
    gop.residual(v, y);
  }

private:
  const F_GFS& f_gfs;
  const C_GFS& c_gfs;

  const F_CC& f_cc;
  const C_CC& c_cc;

  LOP& lop;
  GOP gop;

  const Decomposition& decomp;
};


#endif //BLOCKSTRUCTURED_PRECONDITIONER_RESTRICTION_HH
