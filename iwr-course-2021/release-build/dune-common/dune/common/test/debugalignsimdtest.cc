// generated from debugalignsimdtest.cc.in by cmake -*- buffer-read-only:t -*- vim: set readonly:

#include <config.h>

#include <cstdlib>
#include <type_traits>

#include <dune/common/debugalign.hh>
#include <dune/common/parallel/mpihelper.hh>
#include <dune/common/simd/test.hh>
#include <dune/common/test/debugalignsimdtest.hh>

template<class> struct RebindAccept : std::false_type {};
template<>
struct RebindAccept<Dune::AlignedNumber<double> > : std::true_type {};
template<>
struct RebindAccept<Dune::AlignedNumber<bool> > : std::true_type {};

int main(int argc, char **argv)
{
  Dune::MPIHelper::instance(argc, argv);

  Dune::Simd::UnitTest test;

  using Rebinds = Dune::Simd::RebindList<
    double,
    bool,
    Dune::Simd::EndMark>;

  test.check<Dune::AlignedNumber<double>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();
  test.check<Dune::AlignedNumber<bool>,
             Rebinds, Dune::Std::to_false_type, RebindAccept>();

  return test.good() ? EXIT_SUCCESS : EXIT_FAILURE;
}
