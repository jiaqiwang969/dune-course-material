#ifndef DUNE_CODEGEN_MULADD_WORKAROUNDS_HH
#define DUNE_CODEGEN_MULADD_WORKAROUNDS_HH

/* We are currently having some issues with FMA nodes not being
 * eliminated correctly upon code generation. We "solve" the problem
 * for now with a generic implementation of  the mul_add function.
 */


template<typename T>
inline T mul_add(T op1, T op2, T op3)
{
  return op1 * op2 + op3;
}

#endif
