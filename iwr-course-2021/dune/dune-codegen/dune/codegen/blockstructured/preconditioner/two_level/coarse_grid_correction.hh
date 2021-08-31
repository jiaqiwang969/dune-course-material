#ifndef NEUMANN_NEUMANN_PRECONDITIONER_COARSE_GRID_CORRECTION_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_COARSE_GRID_CORRECTION_HH

#include <dune/istl/preconditioner.hh>
#include <dune/istl/superlu.hh>
#include <dune/istl/solver.hh>
#include <dune/pdelab/backend/istl/bcrsmatrixbackend.hh>
#include <dune/pdelab/gridoperator/gridoperator.hh>

template<typename I, typename R, typename X>
class CoarseGridCorrection : public Dune::Preconditioner<X, X>{
  using DF = double;
  using RT = double;

  using F_X = typename I::F_X;
  using C_X = typename I::C_X;
public:
  using backend = F_X;
  using native = X;

  //! The type of the domain of the operator.
  typedef X domain_type;
  //! The type of the range of the operator.
  typedef X range_type;
  //! The field type of the operator.
  typedef typename X::field_type field_type;

  template<typename C_GFS, typename LOP, typename C_CC>
  CoarseGridCorrection(const I& interpolation_, const R& restriction_, const C_GFS& gfs, const C_CC& cc, LOP& lop)
      : restriction(restriction_), interpolation(interpolation_),
        f_d(interpolation.fine_space()), c_d(interpolation.coarse_space()),
        f_v(interpolation.fine_space()), c_v(interpolation.coarse_space())
  {
    using MB = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
    using GOP = Dune::PDELab::GridOperator<C_GFS, C_GFS, LOP, MB, DF, RT, RT, C_CC, C_CC>;

    GOP gop(gfs, cc, gfs, cc, lop, MB(1));

    typename GOP::Domain x(gop.trialGridFunctionSpace(), 0.);
    typename GOP::Jacobian jac(gop);
    gop.jacobian(x, jac);

    using Dune::PDELab::Backend::native;
    solver.setMatrix(native(jac));
  }

  void pre (X& x, X& b) override {}

  void apply (X& v, const X& d) override {
    using Dune::PDELab::Backend::native;

    const auto& f_gfs = interpolation.fine_space();
    const auto& c_gfs = interpolation.coarse_space();

    f_d = d;

    restriction.apply(f_d, c_d);

    c_v = 0.;
    Dune::InverseOperatorResult res;
    solver.apply(native(c_v), native(c_d), res);

    interpolation.apply(c_v, v);
  }

  void post (X& x) override {}

  [[nodiscard]] Dune::SolverCategory::Category category() const override { return Dune::SolverCategory::sequential; }

private:
  const I& interpolation;
  const R& restriction;

  F_X f_d;
  C_X c_d;
  F_X f_v;
  C_X c_v;

  Dune::SuperLU<Dune::BCRSMatrix<Dune::FieldMatrix<RT, 1, 1>>> solver;
};

#endif //NEUMANN_NEUMANN_PRECONDITIONER_COARSE_GRID_CORRECTION_HH
