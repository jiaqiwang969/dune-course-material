// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:

#ifndef DUNE_BLOCKSTRUCTURED_PRECONDITIONER_ITERATIVE_LOCAL_SOLVER_HH
#define DUNE_BLOCKSTRUCTURED_PRECONDITIONER_ITERATIVE_LOCAL_SOLVER_HH


#include <map>
#include <memory>
#include <dune/common/reservedvector.hh>
#include <dune/istl/solvers.hh>
#include <dune/istl/preconditioners.hh>
#include "local_solver.hh"

template<typename GV, typename LOP, typename RT, typename LocalDecomposition, int k, typename Imp>
class IterativeLocalSolver
  : public LocalSchurSolver<GV, LOP, RT, LocalDecomposition, k,
                            IterativeLocalSolver<GV, LOP, RT, LocalDecomposition, k, Imp>>{
  using Base = LocalSchurSolver<GV, LOP, RT, LocalDecomposition, k,
                                IterativeLocalSolver<GV, LOP, RT, LocalDecomposition, k, Imp>>;
public:
  using V = typename Base::V;
  using EG = typename Base::EG;

  template<typename GFS>
  explicit IterativeLocalSolver(const GV& gv_, const GFS& gfs_, LOP& lop_, const double eps_ = 1e-10)
      : Base(gv_, gfs_, lop_), eps(eps_) {}

  template <typename LFSU, typename LFSV>
  void solveDirichletProblem(const EG& eg, const LFSV& lfsv, V& x, const LFSU& lfsu, V& b) const{
    auto op = asImp().dirichletOperator(eg, lfsu, b, lfsv);
    auto prec = asImp().dirichletPreconditioner(eg, lfsu, b, lfsv);

    Dune::InverseOperatorResult stat;
    Dune::BiCGSTABSolver<V> solver(op, prec, eps, 1000, 0);

    solver.apply(x, b, stat);
  }

  template <typename LFSU, typename LFSV>
  void solveNeumannProblem(const EG& eg, const LFSV& lfsv, V& x, const LFSU& lfsu, V& b) const {
    auto op = asImp().neumannOperator(eg, lfsu, b, lfsv);
    auto prec = asImp().neumannPreconditioner(eg, lfsu, b, lfsv);

    Dune::InverseOperatorResult stat;
    Dune::BiCGSTABSolver<V> solver(op, prec, eps, 1000, 0);

    solver.apply(x, b, stat);
  }
protected:
  Imp& asImp() { return static_cast<Imp &>(*this); }
  const Imp& asImp() const { return static_cast<const Imp &>(*this); }

  double eps;
};

template <typename GV, typename LOP, typename RT, typename LocalDecomposition, int k>
class IterativeMatrixFreeLocalSolver :
    public IterativeLocalSolver<GV, LOP, RT, LocalDecomposition, k,
                                IterativeMatrixFreeLocalSolver<GV, LOP, RT, LocalDecomposition, k>>{
  using Base = IterativeLocalSolver<GV, LOP, RT, LocalDecomposition, k,
                                    IterativeMatrixFreeLocalSolver<GV, LOP, RT, LocalDecomposition, k>>;
public:
  using V = typename Base::V;
  using EG = typename Base::EG;

  using Base::Base;

  template<typename LFSU, typename LFSV>
  struct MatrixFreeOperator : Dune::LinearOperator<V, V>{
    typedef typename V::field_type field_type;

    MatrixFreeOperator(const SolverWrapper<LOP, LocalDecomposition, k>& lop_, const EG& eg_,
                       const LFSU& lfsu_, const LFSV& lfsv_, bool isDirichlet_, double reg_)
        : lop(lop_), eg(eg_), lfsu(lfsu_), lfsv(lfsv_), isDirichlet(isDirichlet_), reg(reg_) {}

    void apply (const V& x, V& y) const override {
      y = 0.;
      lop.jacobian_apply_volume(eg, lfsu, x, lfsv, y, isDirichlet, reg);
    }
    void applyscaleadd (field_type alpha, const V& x, V& y) const override{
      V z(y);
      z = 0.;
      apply(x, z);
      y.axpy(-1., z);
    }
    [[nodiscard]] Dune::SolverCategory::Category category() const override {
      return Dune::SolverCategory::sequential;
    }

  private:
    const SolverWrapper<LOP, LocalDecomposition, k>& lop;
    const EG& eg;
    const LFSU& lfsu;
    const LFSV& lfsv;
    bool isDirichlet;
    double reg;
  };

  template <typename LFSU, typename LFSV>
  MatrixFreeOperator<LFSU, LFSV> dirichletOperator(const EG& eg, const LFSU& lfsu, const V& x, const LFSV& lfsv) const {
    return {this->lopWrapper, eg, lfsu, lfsv, true, 0.};
  }
  template<typename LFSU, typename LFSV>
  MatrixFreeOperator<LFSU, LFSV> neumannOperator(const EG& eg, const LFSU& lfsu, const V& x, const LFSV& lfsv) const {
    static const V ones = ([&x](){ V r(x); r = 1.; return r;})();
    static V norm_inf_v = ([&x](){ V r(x); return r;})();
    norm_inf_v = 0.;
    this->lopWrapper.jacobian_norm_estimate(eg, lfsu, ones, lfsv, norm_inf_v);
    // estimate norm upper bound without assembling the matrix
    const auto norm_ub = *std::max_element(begin(norm_inf_v), end(norm_inf_v),
                                           [](const auto& a, const auto& b){return std::abs(a) < std::abs(b);});
    const auto alpha = (1. + x.N()) / (2 * std::sqrt(x.N())) * norm_ub; // ||A||_inf / sqrt(N) <= ||A||_2 <= sqrt(N) ||A||_inf
    return {this->lopWrapper, eg, lfsu, lfsv, false, alpha * 1e-3};
  }

  template <typename LFSU, typename LFSV>
  Dune::Richardson<V,V> dirichletPreconditioner(const EG& eg, const LFSU& lfsu, const V& x, const LFSV& lfsv) const { return {}; }
  template <typename LFSU, typename LFSV>
  Dune::Richardson<V,V> neumannPreconditioner(const EG& eg, const LFSU& lfsu, const V& x, const LFSV& lfsv) const { return {}; }
};


template <typename GV, typename LOP, typename RT, typename LocalDecomposition, int k>
class IterativeMatrixFreeLocalJacobi :
    public IterativeLocalSolver<GV, LOP, RT, LocalDecomposition, k,
                                IterativeMatrixFreeLocalJacobi<GV, LOP, RT, LocalDecomposition, k>>{
  using Base = IterativeLocalSolver<GV, LOP, RT, LocalDecomposition, k,
                                    IterativeMatrixFreeLocalJacobi<GV, LOP, RT, LocalDecomposition, k>>;
public:
  using V = typename Base::V;
  using EG = typename Base::EG;

  using Base::Base;

  template<typename LFSU, typename LFSV>
  struct MatrixFreeOperator : Dune::LinearOperator<V, V>{
    typedef typename V::field_type field_type;

    MatrixFreeOperator(const SolverWrapper<LOP, LocalDecomposition, k>& lop_, const EG& eg_,
                       const LFSU& lfsu_, const LFSV& lfsv_, bool isDirichlet_)
        : lop(lop_), eg(eg_), isDirichlet(isDirichlet_), lfsu(lfsu_), lfsv(lfsv_) {}

    void apply (const V& x, V& y) const override {
      y = 0.;
      lop.jacobian_apply_volume(eg, lfsu, x, lfsv, y, isDirichlet);
    }
    void applyscaleadd (field_type alpha, const V& x, V& y) const override{
      V z(y);
      z = 0.;
      apply(x, z);
      y.axpy(-1., z);
    }
    [[nodiscard]] Dune::SolverCategory::Category category() const override {
      return Dune::SolverCategory::sequential;
    }

  private:
    const SolverWrapper<LOP, LocalDecomposition, k>& lop;
    const EG& eg;
    const bool isDirichlet;
    const LFSU& lfsu;
    const LFSV& lfsv;
  };

  template <typename LFSU, typename LFSV>
  void solveDirichletProblem(const EG& eg, const LFSV& lfsv, V& x, const LFSU& lfsu, V& b) const{
    static V r(b);
    static V inverse_diagonal(b);

    this->lopWrapper.point_diagonal(eg, lfsu, x, lfsv, inverse_diagonal, true);
    for(auto& val: inverse_diagonal)
      val = 1. / val;

    MatrixFreeOperator<LFSU, LFSV> op(this->lopWrapper, eg, lfsu, lfsv, true);

    for (int i = 0; i < 3; ++i) {
      r = b;
      op.applyscaleadd(-1., x, r);
      for (int it = 0; it < x.size(); ++it) {
        r[it] *= inverse_diagonal[it];
      }
      x += r;
    }
  }

  template <typename LFSU, typename LFSV>
  void solveNeumannProblem(const EG& eg, const LFSV& lfsv, V& x, const LFSU& lfsu, V& b) const {
    static V r(b);
    static V inverse_diagonal(b);

    this->lopWrapper.point_diagonal(eg, lfsu, x, lfsv, inverse_diagonal, false);
    for(auto& val: inverse_diagonal)
      val = 1. / val;

    MatrixFreeOperator<LFSU, LFSV> op(this->lopWrapper, eg, lfsu, lfsv, false);

    for (int i = 0; i < 3; ++i) {
      r = b;
      op.applyscaleadd(-1., x, r);
      for (int it = 0; it < x.size(); ++it) {
        r[it] *= inverse_diagonal[it];
      }
      x += r;
    }
  }
};

#endif //DUNE_BLOCKSTRUCTURED_PRECONDITIONER_ITERATIVE_LOCAL_SOLVER_HH
