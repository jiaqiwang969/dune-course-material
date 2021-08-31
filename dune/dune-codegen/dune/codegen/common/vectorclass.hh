#ifndef DUNE_CODEGEN_COMMON_VECTORCLASS_HH
#define DUNE_CODEGEN_COMMON_VECTORCLASS_HH

#include<dune/codegen/common/simdtraits.hh>

#ifdef ENABLE_COUNTER

#if HAVE_DUNE_OPCOUNTER
#include<dune/opcounter/vectorclass.hh>
#else
#error "dune-opcounter is needed for opcounted vector types"
#endif

#else

#include<dune/codegen/vectorclass/vectorclass.h>
#include<dune/codegen/vectorclass/vectormath_exp.h>
#include<dune/codegen/vectorclass/vectormath_hyp.h>
#include<dune/codegen/vectorclass/vectormath_trig.h>
#include<dune/codegen/common/vcltraits.hh>

#endif

#endif // DUNE_CODEGEN_COMMON_VECTORCLASS_HH
