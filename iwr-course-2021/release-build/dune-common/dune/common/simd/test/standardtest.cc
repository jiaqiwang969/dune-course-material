// generated from standardtest.cc.in by cmake -*- buffer-read-only:t -*- vim: set readonly:

#if HAVE_CONFIG_H
#include "config.h"
#endif

#include <cstdlib>
#include <type_traits>

#include <dune/common/simd/test.hh>
#include <dune/common/simd/test/standardtest.hh>

template<class> struct RebindAccept : std::false_type {};
template<> struct RebindAccept<char> : std::true_type {};
template<> struct RebindAccept<unsigned char> : std::true_type {};
template<> struct RebindAccept<signed char> : std::true_type {};
template<> struct RebindAccept<short> : std::true_type {};
template<> struct RebindAccept<int> : std::true_type {};
template<> struct RebindAccept<long> : std::true_type {};
template<> struct RebindAccept<long long> : std::true_type {};
template<> struct RebindAccept<unsigned short> : std::true_type {};
template<> struct RebindAccept<unsigned> : std::true_type {};
template<> struct RebindAccept<unsigned long> : std::true_type {};
template<> struct RebindAccept<unsigned long long> : std::true_type {};
template<> struct RebindAccept<bool> : std::true_type {};
template<> struct RebindAccept<float> : std::true_type {};
template<> struct RebindAccept<double> : std::true_type {};
template<> struct RebindAccept<long double> : std::true_type {};
template<> struct RebindAccept<std::complex<float>> : std::true_type {};
template<> struct RebindAccept<std::complex<double>> : std::true_type {};
template<> struct RebindAccept<std::complex<long double>> : std::true_type {};

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

  test.check<char, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<unsigned char, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<signed char, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<short, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<int, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<long, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<long long, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<unsigned short, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<unsigned, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<unsigned long, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<unsigned long long, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<bool, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<float, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<double, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<long double, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<std::complex<float>, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<std::complex<double>, Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<std::complex<long double>, Rebinds, Dune::Std::to_false_type, RebindAccept>();

  return test.good() ? EXIT_SUCCESS : EXIT_FAILURE;
}
