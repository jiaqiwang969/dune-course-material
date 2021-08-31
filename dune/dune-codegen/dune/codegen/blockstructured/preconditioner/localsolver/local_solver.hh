// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_PRECONDITIONER_LOCAL_SOLVER_HH
#define DUNE_BLOCKSTRUCTURED_PRECONDITIONER_LOCAL_SOLVER_HH


#include <memory>
#include <dune/common/reservedvector.hh>
#include <dune/common/parametertree.hh>
#include <dune/istl/bdmatrix.hh>
#include "dune/localfunctions/lagrange/lagrangecube.hh"
#include <dune/pdelab/localoperator/flags.hh>
#include <dune/pdelab/common/quadraturerules.hh>
#include <dune/pdelab/common/geometrywrapper.hh>
#include <dune/pdelab/backend/interface.hh>
#include <dune/pdelab/finiteelement/localbasiscache.hh>
#include "wrapper/solver_wrapper.hh"
#include "wrapper/schur_wrapper.hh"

template<typename GV, typename LOP, typename RT, typename LocalDecomposition, int k, typename Imp>
class LocalSchurSolver{
public:
  using V = Dune::BlockVector<RT>;
  using Element = typename GV::Traits::template Codim<0>::Entity;
  using EG = Dune::PDELab::ElementGeometry<Element>;

  template<typename GFS>
  explicit LocalSchurSolver(const GV& gv_, const GFS& gfs_, LOP& lop_)
      : gv(gv_), p_decomp(std::make_shared<LocalDecomposition>(gfs_, gfs_, Dune::ParameterTree{})),
        lopWrapper(lop_, p_decomp), schurWrapper(lop_, p_decomp) {}

  void bind(const EG& eg) { }

  template <typename LFSU, typename LFSV>
  void solveDirichletProblem(const EG& eg, const LFSV& lfsv, V& x, const LFSU& lfsu, V& b) const{
    asImp().solveDirichletProblem(eg, lfsv, x, lfsu, b);
  }

  template <typename LFSU, typename LFSV>
  void solveNeumannProblem(const EG& eg, const LFSV& lfsv, V& x, const LFSU& lfsu, V& b) const {
    asImp().solveNeumannProblem(eg, lfsv, x, lfsu, b);
  }

  template <typename LFSU, typename LFSV>
  void interface_apply(const EG& eg, const LFSU& lfsu, V& x, const LFSV& lfsv, V& b) const {
    schurWrapper.interface_apply(eg, lfsv, x, lfsu, b);
  }

  template <typename LFSU, typename LFSV>
  void interface_cell_apply(const EG& eg, const LFSU& lfsu, V& x, const LFSV& lfsv, V& b) const {
    schurWrapper.interface_cell_apply(eg, lfsv, x, lfsu, b);
  }

  template <typename LFSU, typename LFSV>
  void cell_interface_apply(const EG& eg, const LFSU& lfsu, V& x, const LFSV& lfsv, V& b) const {
    schurWrapper.cell_interface_apply(eg, lfsv, x, lfsu, b);
  }

protected:
  const GV& gv;

  std::shared_ptr<LocalDecomposition> p_decomp;
  SolverWrapper<LOP, LocalDecomposition, k> lopWrapper;
  SchurWrapper<LOP, LocalDecomposition, k> schurWrapper;

private:
  Imp& asImp() { return static_cast<Imp &>(*this); }
  const Imp& asImp() const { return static_cast<const Imp &>(*this); }
};


#endif //DUNE_BLOCKSTRUCTURED_PRECONDITIONER_LOCAL_SOLVER_HH
