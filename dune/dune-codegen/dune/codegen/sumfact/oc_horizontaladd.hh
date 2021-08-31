#ifndef DUNE_CODEGEN_SUMFACT_OCHORIZONTALADD_HH
#define DUNE_CODEGEN_SUMFACT_OCHORIZONTALADD_HH

#include<immintrin.h>
#include<dune/codegen/common/simdtraits.hh>

template<class V>
typename base_floatingpoint<V>::value permuting_horizontal_add_lower(const V& x)
{
  return horizontal_add(x.get_low());
}

template<class V>
typename base_floatingpoint<V>::value permuting_horizontal_add_upper(const V& x)
{
  return horizontal_add(x.get_high());
}

template<class V>
typename base_floatingpoint<V>::value permuting_horizontal_add(const V& x)
{
  return horizontal_add(x);
}

#endif
