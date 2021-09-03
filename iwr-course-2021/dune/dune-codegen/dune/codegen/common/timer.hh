#ifndef DUNE_CODEGEN_COMMON_TIMER_HH
#define DUNE_CODEGEN_COMMON_TIMER_HH

#define _GONE_THROUGH_TIMER_HH

#if ENABLE_CHRONO_TIMER
#include<dune/codegen/common/timer_chrono.hh>
#else
#include<dune/codegen/common/timer_tsc.hh>
#endif

#undef _GONE_THROUGH_TIMER_HH

#endif
