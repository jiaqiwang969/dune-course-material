#ifndef NEUMANN_NEUMANN_PRECONDITIONER_POINT_DIAGONAL_HH
#define NEUMANN_NEUMANN_PRECONDITIONER_POINT_DIAGONAL_HH

#include <dune/localfunctions/lagrange/lagrangecube.hh>
#include <dune/pdelab/finiteelement/localbasiscache.hh>
#include <dune/pdelab/localoperator/flags.hh>
#include <dune/pdelab/common/quadraturerules.hh>

template<int k>
class PointDiagonalLocalOperator : public Dune::PDELab::LocalOperatorDefaultFlags{
public:
  enum { doAlphaVolume = true };

  template<typename GFS>
  PointDiagonalLocalOperator(const GFS &gfs) :
      Q1_microElementBasis() {
    jit = gfs.gridView().template begin<0>()->geometry().jacobianInverseTransposed(Dune::FieldVector<double, 2>());
    detjac = gfs.gridView().template begin<0>()->geometry().integrationElement(Dune::FieldVector<double, 2>());
  }

  template<typename R, typename X, typename EG, typename LFSU, typename LFSV>
  void alpha_volume(const EG &eg, const LFSU &lfsu, const X &x, const LFSV &lfsv, R &r) const {
    auto cell_geo = eg.entity().geometry();
    const auto quadrature_rule = Dune::quadratureRule(cell_geo, 2);

    for (const auto &qp: quadrature_rule) {
      const auto &js_Q1 = cache_Q1.evaluateJacobian(qp.position(), Q1_microElementBasis);
      std::array<JacobianType, 4> grad = {};
      for (int i = 0; i < 4; ++i) {
        jit.usmv(k, js_Q1[i][0], grad[i][0]);
      }
      const double factor = detjac * qp.weight() / double(k * k);
      for (int subel_y = 0; subel_y < k; ++subel_y)
        for (int subel_x = 0; subel_x < k; ++subel_x)
          for (int iy = 0; iy < 2; ++iy)
            for (int ix = 0; ix < 2; ++ix)
              r.accumulate(lfsv, (subel_y + iy) * (k + 1) + subel_x + ix,
                           (grad[ix + iy * 2][0][0] * grad[ix + iy * 2][0][0] +
                            grad[ix + iy * 2][0][1] * grad[ix + iy * 2][0][1]) * factor);
    }
  }

  using Q1_LocalBasis = Dune::Impl::LagrangeCubeLocalBasis<double, double, 2, 1>;
  using JacobianType = typename Q1_LocalBasis::Traits::JacobianType;
  Dune::PDELab::LocalBasisCache<Q1_LocalBasis> cache_Q1;
  const Q1_LocalBasis Q1_microElementBasis;

  Dune::FieldMatrix<double, 2, 2> jit;
  double detjac;
};

#endif //NEUMANN_NEUMANN_PRECONDITIONER_POINT_DIAGONAL_HH
