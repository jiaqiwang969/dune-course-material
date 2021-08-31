#ifndef DUNE_CODEGEN_COMMON_VCLTRAITS_HH
#define DUNE_CODEGEN_COMMON_VCLTRAITS_HH

/** A collection of traits tools for the Vector Class Library */

#include<dune/codegen/common/vectorclass.hh>


template<>
struct base_floatingpoint<Vec2d>
{
  using value = double;
};

template<>
struct base_floatingpoint<Vec4f>
{
  using value = float;
};

template<>
struct simd_size<Vec2d>
{
  static constexpr std::size_t value = 2;
};

template<>
struct simd_size<Vec4f>
{
  static constexpr std::size_t value = 4;
};

#if MAX_VECTOR_SIZE >= 256
template<>
struct base_floatingpoint<Vec4d>
{
  using value = double;
};

template<>
struct base_floatingpoint<Vec8f>
{
  using value = float;
};

template<>
struct simd_size<Vec4d>
{
  static constexpr std::size_t value = 4;
};

template<>
struct simd_size<Vec8f>
{
  static constexpr std::size_t value = 8;
};
#endif

#if MAX_VECTOR_SIZE >= 512
template<>
struct base_floatingpoint<Vec8d>
{
  using value = double;
};

template<>
struct base_floatingpoint<Vec16f>
{
  using value = float;
};

template<>
struct simd_size<Vec8d>
{
  static constexpr std::size_t value = 8;
};

template<>
struct simd_size<Vec16f>
{
  static constexpr std::size_t value = 16;
};

#endif

#endif
