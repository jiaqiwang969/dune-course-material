// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_SOLVER_HH
#define DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_SOLVER_HH

#include <dune/istl/matrix.hh>
#include <dune/istl/solver.hh>
#include <dune/istl/solvers.hh>
#include <dune/istl/preconditioner.hh>
#include <dune/istl/preconditioners.hh>
#include <dune/istl/operators.hh>
#include <dune/istl/io.hh>
#include <dune/common/unused.hh>
#include <dune/pdelab/backend/interface.hh>
#include <dune/common/fmatrix.hh>
#include "operator.hh"
#include "preconditioner.hh"


template<typename OP, typename PC>
class SchurComplement : public Dune::Preconditioner<typename OP::backend, typename OP::backend> {
public:
  using X = typename OP::backend;
  using V = typename OP::native;

  //! \brief The domain type of the preconditioner.
  typedef X domain_type;
  //! \brief The range type of the preconditioner.
  typedef X range_type;
  //! \brief The field type of the preconditioner.
  typedef typename X::field_type field_type;

  SchurComplement(OP& op_, PC& pc_, const bool onlyPrecondition_ = false)
      : op(op_), pc(pc_), onlyPrecondition(onlyPrecondition_) { }

  void pre (X&, X&) override {  }

  void apply (X& v, const X& d) override {
    X rhs = op.computeRHS(d);
    X v_s(rhs); v_s = 0;

    if(onlyPrecondition)
      pc.apply(v_s, rhs);
    else {
      Dune::BiCGSTABSolver<X> solver(op, pc, 1e-10, 1000, 1);

      solver.apply(v_s, rhs, stat);
    }
    op.backTransform(d, v_s, v);
  }

  void post (X&) override { }

  Dune::SolverCategory::Category category() const override {
    return Dune::SolverCategory::sequential;
  }

  auto iterations() const { return stat.iterations; }

private:
  OP& op;
  PC& pc;
  bool onlyPrecondition;
  Dune::InverseOperatorResult stat;
};

#endif //DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_SOLVER_HH
