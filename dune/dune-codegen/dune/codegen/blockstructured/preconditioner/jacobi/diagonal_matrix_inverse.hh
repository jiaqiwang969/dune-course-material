// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef NEUMANN_NEUMANN_PRECONDITIONER_DIAGONAL_MATRIX_INVERSE_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_DIAGONAL_MATRIX_INVERSE_HH

#include <dune/istl/solver.hh>
#include <dune/pdelab/backend/interface.hh>

template<typename X>
class DiagonalMatrixInverse: public Dune::InverseOperator<X, X>{
public:
  explicit DiagonalMatrixInverse(const X& diagonal) : diagonal_inverse(diagonal) {
    using Dune::PDELab::Backend::native;
    for(auto& v: native(diagonal_inverse))
      v = 1. / v;
  }

  void apply (X& x, X& b, Dune::InverseOperatorResult& res) override {
    assert(b.N() == diagonal_inverse.N());
    using Dune::PDELab::Backend::native;
    for (int i = 0; i < native(b).size(); ++i) {
      native(x)[i] = native(diagonal_inverse)[i] * native(b)[i];
    }
  }

  void apply (X& x, X& b, double reduction, Dune::InverseOperatorResult& res) override {
    apply(x, b, res);
  }

  [[nodiscard]] Dune::SolverCategory::Category category() const override {
    return Dune::SolverCategory::sequential;
  }
private:
  X diagonal_inverse;
};

#endif //NEUMANN_NEUMANN_PRECONDITIONER_DIAGONAL_MATRIX_INVERSE_HH
