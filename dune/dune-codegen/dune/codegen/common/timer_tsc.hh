#ifndef DUNE_CODEGEN_COMMON_TIMER_TSC_HH
#define DUNE_CODEGEN_COMMON_TIMER_TSC_HH

#ifndef _GONE_THROUGH_TIMER_HH
#error "Do not include timer_tsc.hh directly, instead use timer.hh"
#endif

#include <dune/codegen/common/tsc.hh>
#include <dune/opcounter/opcounter.hh>

#define HP_TIMER_DURATION(name) __hp_timer_##name##_duration
#define HP_TIMER_STARTTIME(name) __hp_timer_##name##_start
#define HP_TIMER_OPCOUNTERS_START(name) __hp_timer_##name##_counters_start
#define HP_TIMER_OPCOUNTERS(name) __hp_timer_##name##_counters



#ifdef ENABLE_HP_TIMERS

#ifdef ENABLE_COUNTER

#define HP_DECLARE_TIMER(name)                               \
  Dune::PDELab::TSC::Counter HP_TIMER_DURATION(name);	\
  long long HP_TIMER_STARTTIME(name); \
  HP_TIMER_OPCOUNTER::Counters HP_TIMER_OPCOUNTERS_START(name); \
  HP_TIMER_OPCOUNTER::Counters HP_TIMER_OPCOUNTERS(name);

#define HP_TIMER_START(name) \
  do { \
  HP_TIMER_OPCOUNTERS_START(name) = HP_TIMER_OPCOUNTER::counters; \
  HP_TIMER_STARTTIME(name) = Dune::PDELab::TSC::start(); \
  } while(false)

#define HP_TIMER_STOP(name) \
  do { \
  long long __hp_end_time = Dune::PDELab::TSC::stop(); \
  HP_TIMER_OPCOUNTERS(name) += HP_TIMER_OPCOUNTER::counters - HP_TIMER_OPCOUNTERS_START(name); \
  HP_TIMER_DURATION(name) += Dune::PDELab::TSC::elapsed(HP_TIMER_STARTTIME(name),__hp_end_time); \
  } while(false)

#define HP_TIMER_RESET(name) \
  do { \
  HP_TIMER_DURATION(name) = Dune::PDELab::TSC::zero(); \
  HP_TIMER_OPCOUNTERS(name).reset(); \
  } while (false)

#else

#define HP_DECLARE_TIMER(name)                               \
  Dune::PDELab::TSC::Counter HP_TIMER_DURATION(name);	\
  long long HP_TIMER_STARTTIME(name);

#define HP_TIMER_START(name) HP_TIMER_STARTTIME(name) = Dune::PDELab::TSC::start();
#define HP_TIMER_STOP(name) \
  do { \
  long long __hp_end_time = Dune::PDELab::TSC::stop(); \
  HP_TIMER_DURATION(name) += Dune::PDELab::TSC::elapsed(HP_TIMER_STARTTIME(name), __hp_end_time); \
  } while(false)

#define HP_TIMER_RESET(name) HP_TIMER_DURATION(name) = Dune::PDELab::TSC::zero();

#endif // ENABLE_COUNTER

#else // ENABLE_HP_TIMERS

#define HP_DECLARE_TIMER(name)
#define HP_TIMER_START(name)
#define HP_TIMER_STOP(name)
#define HP_TIMER_RESET(name)

#endif // ENABLE_HP_TIMERS




#ifdef ENABLE_COUNTER

#define DUMP_TIMER(level,name,os,reset)\
  { \
    std::string prefix = std::string(#level) + " " + ident + " " + std::string(#name); \
    if (HP_TIMER_DURATION(name) > 1e-12) \
      os << prefix << " time " << Dune::PDELab::TSC::seconds(HP_TIMER_DURATION(name)) << std::endl; \
    HP_TIMER_OPCOUNTERS(name).reportOperations(os,prefix,reset); \
  }

#define DUMP_AND_ACCUMULATE_TIMER(level,name,os,reset,time,ops)  \
  { \
    std::string prefix = std::string(#level) + " " + ident + " " + std::string(#name); \
    if (HP_TIMER_DURATION(name) > 1e-12) \
      os << prefix << " time " << Dune::PDELab::TSC::seconds(HP_TIMER_DURATION(name)) << std::endl; \
    time += HP_TIMER_DURATION(name); \
    ops += HP_TIMER_OPCOUNTERS(name); \
    HP_TIMER_OPCOUNTERS(name).reportOperations(os,prefix,reset); \
  }

#elif defined ENABLE_HP_TIMERS

#define DUMP_TIMER(level,name,os,reset)                       \
  if (HP_TIMER_DURATION(name) > 1e-12) \
    os << #level << " " << ident << " " << #name << " time " << Dune::PDELab::TSC::seconds(HP_TIMER_DURATION(name)) << std::endl; \
  if (reset) HP_TIMER_RESET(name);

#define DUMP_AND_ACCUMULATE_TIMER(level, name,os,reset,time,ops)  \
  if (HP_TIMER_DURATION(name) > 1e-12) \
    os << #level << " " << ident << " " << #name << " time " << Dune::PDELab::TSC::seconds(HP_TIMER_DURATION(name)) << std::endl; \
  time += HP_TIMER_DURATION(name); \
  if (reset) HP_TIMER_RESET(name);

#else

#define DUMP_TIMER(level,name,os,reset)
#define DUMP_AND_ACCUMULATE_TIMER(level,name,os,reset,time,ops)

#endif

#endif // DUNE_CODEGEN_COMMON_TIMER_TSC_HH
