// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_SCHUR_COMPLEMENT_SCHUR_COMPLEMENTS_HH
#define DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_SCHUR_COMPLEMENT_SCHUR_COMPLEMENTS_HH

#include <iostream>
#include <random>
#include <memory>
#include <dune/istl/matrix.hh>
#include <dune/istl/solver.hh>
#include <dune/istl/solvers.hh>
#include <dune/istl/btdmatrix.hh>
#include <dune/istl/preconditioner.hh>
#include <dune/istl/preconditioners.hh>
#include <dune/istl/operators.hh>
#include <dune/istl/superlu.hh>
#include <dune/istl/io.hh>
#include <dune/istl/paamg/amg.hh>
#include <dune/common/unused.hh>
#include <dune/pdelab/backend/interface.hh>
#include <dune/geometry/typeindex.hh>
#include <dune/common/fmatrix.hh>
#include <dune/istl/bdmatrix.hh>


template<typename GO_NN, typename Decomposition, typename X>
class NeumannNeumann : public Dune::Preconditioner<X, X> {
public:
  using backend = typename GO_NN::Domain;
  using native = X;

  //! The type of the domain of the operator.
  typedef X domain_type;
  //! The type of the range of the operator.
  typedef X range_type;
  //! The field type of the operator.
  typedef typename X::field_type field_type;

  NeumannNeumann(const GO_NN& go_nn_, const Decomposition& decomp_)
      : go_nn(go_nn_), decomp(decomp_),
        d_backend(go_nn.trialGridFunctionSpace()), v_backend(go_nn.testGridFunctionSpace()) { }

  void pre (X& x, X& b) override {}

  void apply (X& v, const X& d) override {
    using Dune::PDELab::Backend::native;

    d_backend = 0.;
    decomp.copyInteriorBoundary(d, d_backend);
    decomp.scale(d_backend);

    v_backend = 0.;
    go_nn.residual(d_backend, v_backend);

    decomp.copyInteriorBoundary(v_backend, v);
    decomp.scale(v);
  }

  void post (X& x) override {}

  [[nodiscard]] Dune::SolverCategory::Category category() const override {
    return Dune::SolverCategory::sequential;
  }

private:
  const GO_NN& go_nn;
  const Decomposition& decomp;
  backend d_backend;
  backend v_backend;
};


template<typename Decomposition, typename P>
class PreconditionerWrapper: public Dune::Preconditioner<typename P::domain_type, typename P::range_type>{
public:
  using domain_type = typename P::domain_type;
  using range_type = typename P::range_type;

  using X = domain_type;
  using Y = range_type;

  template<typename... Args>
  explicit PreconditionerWrapper(const Decomposition& decomp_, Args&&... args)
      : decomp(decomp_), prec(std::forward<Args>(args)...){ }


  void pre (X& x, X& b) override {}

  void apply (X& v, const Y& d) override {
    Y d_copy(d);
    X v_copy(v);

    d_copy = 0.;
    decomp.copyInteriorBoundary(d, d_copy);

    prec.apply(v_copy, d_copy);

    v = 0.;
    decomp.copyInteriorBoundary(v_copy, v);
  }

  void post (X& x) override {}

  [[nodiscard]] Dune::SolverCategory::Category category() const override {
    return prec.category();
  }

private:
  P prec;
  const Decomposition& decomp;
};

#endif //DUNE_BLOCKSTRUCTURED_SCHUR_COMPLEMENT_SCHUR_COMPLEMENT_SCHUR_COMPLEMENTS_HH
