#ifndef DUNE_CODEGEN_SUMFACT_HORIZONTALADD_HH
#define DUNE_CODEGEN_SUMFACT_HORIZONTALADD_HH

#include<dune/codegen/common/vectorclass.hh>


// Only use our custom implementations if we have AVX2 or later!
#if INSTRSET >= 8

/** Implement a variant of horizontal_add(Vec2d) that avoids the haddpd
 *  instruction and instead uses the shuffle port.
 */
static inline double permuting_horizontal_add (const Vec2d & a)
{
    return _mm_cvtsd_f64(_mm_add_pd(_mm_permute_pd(a,1),a));
}

/** Implement a variant of horizontal_add(Vec4d) that avoids the haddpd
 *  instruction and instead uses the shuffle port.
 */
static inline double permuting_horizontal_add (const Vec4d& a)
{
    __m128d valupper = _mm256_extractf128_pd(a, 1);
    __m128d vallower = _mm256_castpd256_pd128(a);
    __m128d valval = _mm_add_pd(valupper, vallower);
    __m128d res = _mm_add_pd(_mm_permute_pd(valval,1), valval);
    return _mm_cvtsd_f64(res);
}

#if MAX_VECTOR_SIZE >= 512

/** Implement a variant of horizontal_add(Vec8d) that avoids the haddpd
 *  instruction and instead uses the shuffle port.
 */
static inline double permuting_horizontal_add(const Vec8d& a)
{
  return permuting_horizontal_add(a.get_low() + a.get_high());
}

#endif

#else
template<typename V>
static inline double permuting_horizontal_add (const V& a)
{
    return horizontal_add(a);
}

#endif

template<class V>
typename base_floatingpoint<V>::value horizontal_add_lower(const V& x)
{
  return horizontal_add(x.get_low());
}

template<class V>
typename base_floatingpoint<V>::value horizontal_add_upper(const V& x)
{
  return horizontal_add(x.get_high());
}

template<class V>
typename base_floatingpoint<V>::value permuting_horizontal_add_lower(const V& x)
{
  return permuting_horizontal_add(x.get_low());
}

template<class V>
typename base_floatingpoint<V>::value permuting_horizontal_add_upper(const V& x)
{
  return permuting_horizontal_add(x.get_high());
}

#endif
