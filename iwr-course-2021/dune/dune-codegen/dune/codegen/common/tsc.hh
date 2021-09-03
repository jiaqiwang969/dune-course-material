#ifndef DUNE_CODEGEN_COMMON_TSC_TIMER_HH
#define DUNE_CODEGEN_COMMON_TSC_TIMER_HH

#include <dune/pdelab/common/exceptions.hh>
#include <dune/common/parametertree.hh>

namespace Dune
{
  namespace PDELab
  {

    class TSCError
        : public Exception
    {
    };

    class TSCNotInKernelLog
        : public TSCError
    {
    };

    class TSC
    {

    public:
      using Counter = std::uint64_t;

      static constexpr std::size_t calibrationIterations()
      {
        return 100000;
      }

      // static Counter start()
      // {
      //   unsigned a, d;
      //   asm volatile(
      //                "lfence\n"
      //                "rdtsc"
      //                :"=a" (a), "=d" (d)
      //                ::
      //                );
      //   return (static_cast<std::uint64_t>(d) << 32) | a;
      // }

      // static Counter stop()
      // {
      //   unsigned a, d;
      //   asm volatile(
      //                "lfence\n"
      //                "rdtsc"
      //                :"=a" (a), "=d" (d)
      //                ::
      //                );
      //   return (static_cast<std::uint64_t>(d) << 32) | a;
      // }

      static Counter zero()
      {
        return 0;
      }

      static void init()
      {
        instance(nullptr);
      }

      static void init(const Dune::ParameterTree &params)
      {
        instance(&params);
      }

      static Counter overhead()
      {
        return instance()._overhead;
      }

      static Counter frequency()
      {
        return instance()._frequency;
      }

      static Counter elapsed(Counter begin, Counter end)
      {
        return end - begin - _overhead;
      }

      static double seconds(Counter elapsed)
      {
        return elapsed * instance()._scale_factor;
      }

      TSC(const TSC &) = delete;
      TSC(TSC &&) = delete;
      TSC &operator=(const TSC &) = delete;
      TSC &operator=(TSC &&) = delete;

    private:
      static const TSC &instance(const Dune::ParameterTree *params = nullptr)
      {
        static TSC tsc(params);
        return tsc;
      }

      TSC(const Dune::ParameterTree *params);

      Counter _frequency;
      double _scale_factor;

      // make this static to avoid the overhead of calling instance everytime we evaluate a timer
      static Counter _overhead;
    };

  } // namespace PDELab
} // namespace Dune

#endif // DUNE_PDELAB_COMMON_TSC_HH
