// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_SCHUR_RHS_LOP_HH
#define DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_SCHUR_RHS_LOP_HH


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


template<typename GV, typename LS, typename RT, int k>
struct SchurRHSOperator
    : public Dune::PDELab::LocalOperatorDefaultFlags {
  enum { doAlphaVolume = true };

  SchurRHSOperator(const GV& gv_, LS& ls)
      : gv(gv_), localSolver(ls){ }

  template<typename R, typename X, typename EG, typename LFSU, typename LFSV>
  void alpha_volume(const EG &eg, const LFSU &lfsu, const X &x, const LFSV &lfsv, R &r) const {
    localSolver.bind(eg);

    const std::size_t size = x.size();
    using Vector = Dune::BlockVector<RT>;
    static Vector f(size), d(size), v(size);

    std::copy_n(begin(accessBaseContainer(x)), size, begin(d));

    v = 0.;
    localSolver.solveDirichletProblem(eg, lfsv, v, lfsu, d);

    // K_BI * v
    f = 0.;
    localSolver.interface_cell_apply(eg, lfsu, v, lfsv, f);

    std::transform(begin(f), end(f), begin(accessBaseContainer(r)), [](const auto& a) { return -1 * a; });
  }

private:
  const GV& gv;
  LS& localSolver;
};

#endif //DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_SCHUR_RHS_LOP_HH
