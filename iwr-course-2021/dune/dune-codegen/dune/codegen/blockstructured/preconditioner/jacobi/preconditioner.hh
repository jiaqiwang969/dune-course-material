// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef NEUMANN_NEUMANN_PRECONDITIONER_PRECONDITIONER_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_PRECONDITIONER_HH

#include <dune/istl/preconditioner.hh>
#include <dune/istl/operators.hh>
#include <dune/istl/solver.hh>

template<typename X>
class JacobiPreconditioner : public Dune::Preconditioner<X, X>{
public:
  JacobiPreconditioner(Dune::LinearOperator<X, X>& op_,
                       Dune::InverseOperator<X, X>& inverse_point_diagonal_)
      : op(op_), inverse_point_diagonal(inverse_point_diagonal_) {}

  void pre (X& x, X& b) override {}

  void apply (X& v, const X& d) override {
    static X r(d), u(d);
    for (int i = 0; i < 3; ++i) {
      r = d;
      op.applyscaleadd(-1., v, r);
      Dune::InverseOperatorResult res{};
      inverse_point_diagonal.apply(u, r, res);
      v += u;
    }
  }

  void post (X& x) override {}

  [[nodiscard]] Dune::SolverCategory::Category category() const override {
    return Dune::SolverCategory::sequential;
  }
private:
  Dune::LinearOperator<X, X>& op;
  Dune::InverseOperator<X, X>& inverse_point_diagonal;
};

#endif //NEUMANN_NEUMANN_PRECONDITIONER_PRECONDITIONER_HH
