// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_POISSON_NN_LOP_HH
#define DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_POISSON_NN_LOP_HH


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
struct NeumannNeumannOperator
    : public Dune::PDELab::LocalOperatorDefaultFlags {
  enum { doAlphaVolume = true };

  NeumannNeumannOperator(const GV& gv_, LS& ls)
      : gv(gv_), localSolver(ls){  }

  template<typename R, typename X, typename EG, typename LFSU, typename LFSV>
  void alpha_volume(const EG &eg, const LFSU &lfsu, const X &x, const LFSV &lfsv, R &r) const {
    const std::size_t size = x.size();
    using Vector = Dune::BlockVector<RT>;
    static Vector v(size), d(size);

    std::copy_n(begin(accessBaseContainer(x)), size, begin(d));

    localSolver.bind(eg);

    v = 0.;
    localSolver.solveNeumannProblem(eg, lfsv, v, lfsu, d);

    std::copy_n(begin(v), size, begin(accessBaseContainer(r)));
  }

private:
  const GV& gv;
  LS& localSolver;
};

#endif //DUNE_BLOCKSTRUCTURED_PRECONDITIONER_POISSON_POISSON_NN_LOP_HH
