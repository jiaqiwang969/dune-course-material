#ifndef DUNE_CODEGEN_CACHEWRAPPER_HH
#define DUNE_CODEGEN_CACHEWRAPPER_HH

#include<vector>

#include<dune/pdelab/finiteelement/localbasiscache.hh>

/**
 * A wrapper to the LocalBasisCache from PDELab, that does return references
 * to std::vectors, but instead returns a proxy object, that has an operator[]
 * (but no other functionality).
 *
 * This was necessary in code generation, as temporaries need to be pre-declared
 * in loopy and it is not possible to do that with references.
 */


template<typename T>
class CacheReturnProxy
{
  public:
  CacheReturnProxy(const std::vector<T>* _v = 0) : v(_v)
  {}

  const T& operator[](std::size_t i) const
  {
    return (*v)[i];
  }

  private:
  const std::vector<T>* v;
};


template<typename LocalBasisType >
class LocalBasisCacheWithoutReferences
{
  using Cache = typename Dune::PDELab::LocalBasisCache<LocalBasisType>;
  using DomainFieldType = typename LocalBasisType::Traits::DomainFieldType;
  using DomainType = typename LocalBasisType::Traits::DomainType;
  using RangeType = typename LocalBasisType::Traits::RangeType;
  using JacobianType = typename LocalBasisType::Traits::JacobianType;

  public:
  using FunctionReturnType = CacheReturnProxy<RangeType>;
  using JacobianReturnType = CacheReturnProxy<JacobianType>;

  FunctionReturnType evaluateFunction(const DomainType& position, const LocalBasisType& localbasis) const
  {
    return FunctionReturnType(&c.evaluateFunction(position, localbasis));
  }

  JacobianReturnType evaluateJacobian(const DomainType& position, const LocalBasisType& localbasis) const
  {
    return JacobianReturnType(&c.evaluateJacobian(position, localbasis));
  }

  private:
  Cache c;
};


template <typename G, typename T>
void fillQuadratureWeightsCache(const G& geo, const int quadOrder, T& quadratureWeights){
  if(quadratureWeights.size() != 0)
    return;
  else{
    for (const auto& qp : quadratureRule(geo, quadOrder)){
      quadratureWeights.push_back(qp.weight());
    }
  }
}


template <typename G, typename T>
void fillQuadraturePointsCache(const G& geo, const int quadOrder, T& quadraturePoints){
  if(quadraturePoints.size() != 0)
    return;
  else{
    for (const auto& qp : quadratureRule(geo, quadOrder)){
      quadraturePoints.push_back(qp.position());
    }
  }
}

#endif
