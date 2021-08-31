#ifndef BLOCKSTRUCTURED_PRECONDITIONER_DECOMPOSITION_HH
#define BLOCKSTRUCTURED_PRECONDITIONER_DECOMPOSITION_HH

#include <algorithm>
#include <dune/pdelab/localoperator/flags.hh>
#include <dune/pdelab/gridoperator/gridoperator.hh>
#include <dune/pdelab/backend/istl.hh>


template<typename GFS, typename CC>
class SchurDecomposition{
  using DF = double;
  using RT = double;

  class DomainCountLocalOperator: public Dune::PDELab::LocalOperatorDefaultFlags{
  public:
    static constexpr bool doAlphaVolume = true;

    template<typename R, typename X, typename EG, typename LFSU, typename LFSV>
    void alpha_volume(const EG &eg, const LFSU &lfsu, const X &x, const LFSV &lfsv, R &r) const {
      auto& r_data = accessBaseContainer(r);
      std::fill(begin(r_data), end(r_data), 1.);
    }
  };

  using MB = Dune::PDELab::ISTL::BCRSMatrixBackend<>;
  using GOP = Dune::PDELab::GridOperator<GFS, GFS, DomainCountLocalOperator, MB, DF, RT, RT, CC, CC>;

  using X = typename GOP::Domain;
  using V = typename Dune::PDELab::Backend::Native<X>;

public:
  explicit SchurDecomposition(const GFS& gfs, const CC& cc) {
    using Dune::PDELab::Backend::native;
    DomainCountLocalOperator lop{};
    GOP gop(gfs, cc, gfs, cc, lop, MB(1));

    X zero(gfs, 0.), domainCount(gfs, 0.);
    gop.residual(zero, domainCount);

    auto interior_boundary_node_pred = [] (const auto& a) {return a>1.;};
    const auto interiorBoundarySize = std::count_if(begin(native(domainCount)), end(native(domainCount)),
                                                    interior_boundary_node_pred);
    inverseDomainCount.resize(interiorBoundarySize);

    interiorBoundaryNodes.reserve(interiorBoundarySize);
    interiorNodes.reserve(domainCount.N() - interiorBoundarySize);

    for (std::size_t i = 0; i < domainCount.N(); ++i)
      if(interior_boundary_node_pred(native(domainCount)[i]))
        interiorBoundaryNodes.push_back(i);
      else
        interiorNodes.push_back(i);

    for (int i = 0; i < interiorBoundarySize; ++i)
      inverseDomainCount[i] = 1. / native(domainCount)[interiorBoundaryNodes[i]];

    std::cout << "decomposition with " << interiorBoundarySize << " interior boundary dofs generated" << std::endl;
  }

  void copyInteriorBoundary(const X& src, V& dest) const {
    using Dune::PDELab::Backend::native;
    for (std::size_t i = 0; i < interiorBoundaryNodes.size(); ++i)
      dest[i] = native(src)[interiorBoundaryNodes[i]];
  }

  void copyInteriorBoundary(const V &src, X &dest) const {
    using Dune::PDELab::Backend::native;
    for (std::size_t i = 0; i < interiorBoundaryNodes.size(); ++i)
      native(dest)[interiorBoundaryNodes[i]] = src[i];
  }

  void copyInteriorBoundary(const X& src, X& dest) const {
    using Dune::PDELab::Backend::native;
    for (std::size_t i = 0; i < interiorBoundaryNodes.size(); ++i)
      native(dest)[interiorBoundaryNodes[i]] = native(src)[interiorBoundaryNodes[i]];
  }

  void copyInteriorBoundary(const V &src, V &dest) const {
    for (std::size_t i = 0; i < interiorBoundaryNodes.size(); ++i)
      dest[i] = src[i];
  }

  void scale(X& x) const{
    using Dune::PDELab::Backend::native;
    for (std::size_t i = 0; i < interiorBoundaryNodes.size(); ++i)
      native(x)[interiorBoundaryNodes[i]] *= inverseDomainCount[i];
  }

  void scale(V& x) const{
    for (std::size_t i = 0; i < interiorBoundaryNodes.size(); ++i)
      x[i] *= inverseDomainCount[i];
  }

  std::size_t size() const { return interiorBoundaryNodes.size();}

public:
  V inverseDomainCount;
  std::vector<std::size_t> interiorBoundaryNodes, interiorNodes;
};

#endif //BLOCKSTRUCTURED_PRECONDITIONER_DECOMPOSITION_HH
