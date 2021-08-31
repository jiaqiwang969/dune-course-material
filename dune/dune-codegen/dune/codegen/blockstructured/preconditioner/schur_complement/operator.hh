// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_OPERATOR_HH
#define DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_OPERATOR_HH

#include <dune/istl/matrix.hh>
#include <dune/istl/btdmatrix.hh>
#include <dune/istl/operators.hh>
#include <dune/istl/umfpack.hh>
#include <dune/common/unused.hh>
#include <dune/pdelab/backend/interface.hh>
#include <dune/geometry/typeindex.hh>
#include <dune/common/fmatrix.hh>
#include <dune/istl/solver.hh>
#include <dune/istl/io.hh>


template<typename GO_APPLY, typename GO_RHS, typename GO_BACK_TRAFO, typename Decomposition, typename X>
class SchurOperatorMatrixFree:
    public Dune::LinearOperator<X, X> {
public:
  using V = Dune::PDELab::Backend::Native<X>;
  //! The type of the domain of the operator.
  typedef V domain_type;
  //! The type of the range of the operator.
  typedef V range_type;
  //! The field type of the operator.
  typedef typename V::field_type field_type;

  using backend = X;
  using native = V;

  using GO = GO_APPLY;

  using M = Dune::PDELab::Backend::Native<typename GO::Jacobian>;

  using size_type = typename M::size_type;

  SchurOperatorMatrixFree(GO_APPLY& go_apply_, GO_RHS& go_rhs_, GO_BACK_TRAFO& go_back_trafo_,
                          const Decomposition& decomp_)
      : go_apply(go_apply_), go_rhs(go_rhs_), go_back_trafo(go_back_trafo_),
        x_backend(go_apply.trialGridFunctionSpace()), y_backend(go_apply.trialGridFunctionSpace()),
        decomp(decomp_)
  { }

  /*! \brief apply operator to x:  \f$ y = A(x) \f$
        The input vector is consistent and the output must also be
     consistent on the interior+border partition.
   */
  void apply (const X& x, X& y) const override {
    x_backend = 0.;
    decomp.copyInteriorBoundary(x, x_backend);

    y_backend = 0.;
    go_apply.residual(x_backend, y_backend);

    decomp.copyInteriorBoundary(y_backend, y);
  }
  //! apply operator to x, scale and add:  \f$ y = y + \alpha A(x) \f$
  void applyscaleadd (field_type alpha, const X& x, X& y) const override{
    X z(y);

    apply(x, z);

    y.axpy(alpha, z);
  }

  Dune::SolverCategory::Category category() const override {
    return Dune::SolverCategory::sequential;
  }

  X computeRHS(const X& b){
    X b_backend(b);

    y_backend = 0.;
    decomp.copyInteriorBoundary(b, y_backend);

    go_rhs.residual(b_backend, y_backend);

    X b_s(go_apply.testGridFunctionSpace(), 0.);
    decomp.copyInteriorBoundary(y_backend, b_s);

    return b_s;
  }

  void backTransform(const X& b, const X& u_s, X& u){
    X b_backend(b);
    decomp.copyInteriorBoundary(u_s, b_backend);

    y_backend = 0.;
    go_back_trafo.residual(b_backend, y_backend);

    u = y_backend;
    decomp.copyInteriorBoundary(u_s, u);
  }

public:

  GO_APPLY& go_apply;
  GO_RHS& go_rhs;
  GO_BACK_TRAFO& go_back_trafo;
  mutable X x_backend;
  mutable X y_backend;
  const Decomposition& decomp;
};

#endif //DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_OPERATOR_HH
