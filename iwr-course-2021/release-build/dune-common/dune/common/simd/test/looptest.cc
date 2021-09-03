// generated from looptest.cc.in by cmake -*- buffer-read-only:t -*- vim: set readonly:

#if HAVE_CONFIG_H
#include "config.h"
#endif

#include <cstdlib>
#include <type_traits>

#include <dune/common/simd/loop.hh>
#include <dune/common/simd/test.hh>
#include <dune/common/simd/test/looptest.hh>
#include <dune/common/std/type_traits.hh>

template<class> struct RebindAccept : std::false_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<char, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<unsigned char, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<signed char, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<short, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<int, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<long, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<long long, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<unsigned short, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<unsigned, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<unsigned long, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<unsigned long long, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<bool, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<float, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<double, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<long double, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<std::complex<float>, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<std::complex<double>, 5> > : std::true_type {};
template<>
struct RebindAccept<Dune::LoopSIMD<std::complex<long double>, 5> > : std::true_type {};

using Rebinds = Dune::Simd::RebindList<
  char,
  unsigned char,
  signed char,
  short,
  int,
  long,
  long long,
  unsigned short,
  unsigned,
  unsigned long,
  unsigned long long,
  bool,
  float,
  double,
  long double,
  std::complex<float>,
  std::complex<double>,
  std::complex<long double>,
  Dune::Simd::EndMark>;

int main()
{
  Dune::Simd::UnitTest test;

  test.check<Dune::LoopSIMD<char, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<unsigned char, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<signed char, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<short, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<int, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<long, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<long long, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<unsigned short, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<unsigned, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<unsigned long, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<unsigned long long, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<bool, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<float, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<double, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<long double, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<std::complex<float>, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<std::complex<double>, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::LoopSIMD<std::complex<long double>, 5>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();

  return test.good() ? EXIT_SUCCESS : EXIT_FAILURE;
}
