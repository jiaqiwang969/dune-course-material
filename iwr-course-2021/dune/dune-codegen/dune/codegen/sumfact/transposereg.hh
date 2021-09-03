#ifndef DUNE_CODEGEN_SUMFACT_TRANSPOSEREG_HH
#define DUNE_CODEGEN_SUMFACT_TRANSPOSEREG_HH

#include<dune/codegen/common/vectorclass.hh>

// DOUBLE 2 x 2
void transpose_reg(Vec2d& a0, Vec2d& a1)
{
  auto tmp = a0[1];
  a0 = Vec2d(a0[0], a1[0]);
  a1 = Vec2d(tmp, a1[1]);
}

// FLOAT 4 x 2
void transpose_reg(Vec4f& a0, Vec4f& a1)
{
  Vec4f b0, b1;
  b0 = blend4<0,1,4,5>(a0,a1);
  b1 = blend4<2,3,6,7>(a0,a1);
  a0 = b0;
  a1 = b1;
}

// FLOAT 4 x 4
void transpose_reg(Vec4f& a0, Vec4f& a1, Vec4f& a2, Vec4f& a3)
{
  Vec4f b0,b1,b2,b3;
  b0 = blend4<0,4,2,6>(a0,a1);
  b1 = blend4<1,5,3,7>(a0,a1);
  b2 = blend4<0,4,2,6>(a2,a3);
  b3 = blend4<1,5,3,7>(a2,a3);
  a0 = blend4<0,1,4,5>(b0,b2);
  a1 = blend4<0,1,4,5>(b1,b3);
  a2 = blend4<2,3,6,7>(b0,b2);
  a3 = blend4<2,3,6,7>(b1,b3);
}

#if MAX_VECTOR_SIZE >= 256

// DOUBLE 4 x 2
void transpose_reg(Vec4d& a0, Vec4d& a1)
{
  Vec4d b0, b1;
  b0 = blend4<0,1,4,5>(a0,a1);
  b1 = blend4<2,3,6,7>(a0,a1);
  a0 = b0;
  a1 = b1;
}

// DOUBLE 4 x 4
void transpose_reg(Vec4d& a0, Vec4d& a1, Vec4d& a2, Vec4d& a3)
{
  Vec4d b0,b1,b2,b3;
  b0 = blend4<0,4,2,6>(a0,a1);
  b1 = blend4<1,5,3,7>(a0,a1);
  b2 = blend4<0,4,2,6>(a2,a3);
  b3 = blend4<1,5,3,7>(a2,a3);
  a0 = blend4<0,1,4,5>(b0,b2);
  a1 = blend4<0,1,4,5>(b1,b3);
  a2 = blend4<2,3,6,7>(b0,b2);
  a3 = blend4<2,3,6,7>(b1,b3);
}

// FLOAT 8 x 2
void transpose_reg (Vec8f& a0, Vec8f& a1)
{
  Vec8f b0, b1;
  b0 = blend8<0,1,2,3,8,9,10,11>(a0, a1);
  b1 = blend8<4,5,6,7,12,13,14,15>(a0, a1);
  a0 = b0;
  a1 = b1;
}

// FLOAT 8 x 4
void transpose_reg(Vec8f& a0, Vec8f& a1, Vec8f& a2, Vec8f& a3)
{
  Vec8f b0, b1, b2, b3;
  b0 = blend8<0,1,8,9,2,3,10,11>(a0, a1);
  b1 = blend8<4,5,12,13,6,7,14,15>(a0, a1);
  b2 = blend8<0,1,8,9,2,3,10,11>(a2, a3);
  b3 = blend8<4,5,12,13,6,7,14,15>(a2, a3);
  a0 = blend8<0,1,2,3,8,9,10,11>(b0, b2);
  a1 = blend8<4,5,6,7,12,13,14,15>(b0, b2);
  a2 = blend8<0,1,2,3,8,9,10,11>(b1, b3);
  a3 = blend8<4,5,6,7,12,13,14,15>(b1, b3);
}

namespace impl
{
  /* (alow, aupp), (blow, bupp) -> (alow, blow), (aupp, bupp) */
  void swap_halves(Vec8f& a, Vec8f& b)
  {
    Vec4f tmp = a.get_high();
    a = Vec8f(a.get_low(), b.get_low());
    b = Vec8f(tmp, b.get_high());
  }

  /* A 4x8 transpose that behaves exactly like Vec4d's 4x4 transpose
   * on the lower and upper halves of the Vec8d
   */
  void _transpose4x8(Vec8f& a0, Vec8f& a1, Vec8f& a2, Vec8f& a3)
  {
    Vec8f b0,b1,b2,b3;
    b0 = blend8<0,8,2,10,4,12,6,14>(a0,a1);
    b1 = blend8<1,9,3,11,5,13,7,15>(a0,a1);
    b2 = blend8<0,8,2,10,4,12,6,14>(a2,a3);
    b3 = blend8<1,9,3,11,5,13,7,15>(a2,a3);
    a0 = blend8<0,1,8,9,4,5,12,13>(b0,b2);
    a1 = blend8<0,1,8,9,4,5,12,13>(b1,b3);
    a2 = blend8<2,3,10,11,6,7,14,15>(b0,b2);
    a3 = blend8<2,3,10,11,6,7,14,15>(b1,b3);
  }
}

// FLOAT 8 x 8
void transpose_reg(Vec8f& a0, Vec8f& a1, Vec8f& a2, Vec8f& a3,
                   Vec8f& a4, Vec8f& a5, Vec8f& a6, Vec8f& a7)
{
  impl::_transpose4x8(a0,a1,a2,a3);
  impl::_transpose4x8(a4,a5,a6,a7);
  impl::swap_halves(a0,a4);
  impl::swap_halves(a1,a5);
  impl::swap_halves(a2,a6);
  impl::swap_halves(a3,a7);
}

#endif

#if MAX_VECTOR_SIZE >= 512

// DOUBLE 8 x 4
void transpose_reg(Vec8d& a0, Vec8d& a1, Vec8d& a2, Vec8d& a3)
{
  Vec8d b0, b1, b2, b3;
  b0 = blend8<0,1,8,9,2,3,10,11>(a0, a1);
  b1 = blend8<4,5,12,13,6,7,14,15>(a0, a1);
  b2 = blend8<0,1,8,9,2,3,10,11>(a2, a3);
  b3 = blend8<4,5,12,13,6,7,14,15>(a2, a3);
  a0 = blend8<0,1,2,3,8,9,10,11>(b0, b2);
  a1 = blend8<4,5,6,7,12,13,14,15>(b0, b2);
  a2 = blend8<0,1,2,3,8,9,10,11>(b1, b3);
  a3 = blend8<4,5,6,7,12,13,14,15>(b1, b3);
}

// DOUBLE 8 x 2
/** TODO: Is this transpose using blend8d superior to the swap_halves
 *        version below using get_low/get_high?
 */
void transpose_reg (Vec8d& a0, Vec8d& a1)
{
  Vec8d b0, b1;
  b0 = blend8<0,1,2,3,8,9,10,11>(a0, a1);
  b1 = blend8<4,5,6,7,12,13,14,15>(a0, a1);
  a0 = b0;
  a1 = b1;
}

namespace impl
{
  /* (alow, aupp), (blow, bupp) -> (alow, blow), (aupp, bupp) */
  void swap_halves(Vec8d& a, Vec8d& b)
  {
    Vec4d tmp = a.get_high();
    a = Vec8d(a.get_low(), b.get_low());
    b = Vec8d(tmp, b.get_high());
  }

  /* A 4x8 transpose that behaves exactly like Vec4d's 4x4 transpose
   * on the lower and upper halves of the Vec8d
   */
  void _transpose4x8(Vec8d& a0, Vec8d& a1, Vec8d& a2, Vec8d& a3)
  {
    Vec8d b0,b1,b2,b3;
    b0 = blend8<0,8,2,10,4,12,6,14>(a0,a1);
    b1 = blend8<1,9,3,11,5,13,7,15>(a0,a1);
    b2 = blend8<0,8,2,10,4,12,6,14>(a2,a3);
    b3 = blend8<1,9,3,11,5,13,7,15>(a2,a3);
    a0 = blend8<0,1,8,9,4,5,12,13>(b0,b2);
    a1 = blend8<0,1,8,9,4,5,12,13>(b1,b3);
    a2 = blend8<2,3,10,11,6,7,14,15>(b0,b2);
    a3 = blend8<2,3,10,11,6,7,14,15>(b1,b3);
  }
}

// DOUBLE 8 x 8
/* This is the 8x8 transpose of Vec8d's. It uses the same shuffling
 * as Vec4d, but on the 4x4 subblocks. Afterwards, the off diagonal
 * blocks are swapped.
 */
void transpose_reg(Vec8d& a0, Vec8d& a1, Vec8d& a2, Vec8d& a3,
                   Vec8d& a4, Vec8d& a5, Vec8d& a6, Vec8d& a7)
{
  impl::_transpose4x8(a0,a1,a2,a3);
  impl::_transpose4x8(a4,a5,a6,a7);
  impl::swap_halves(a0,a4);
  impl::swap_halves(a1,a5);
  impl::swap_halves(a2,a6);
  impl::swap_halves(a3,a7);
}

void swap_halves(Vec16f& a0, Vec16f& a1)
{
  Vec8f tmp = a0.get_high();
  a0 = Vec16f(a0.get_low(), a1.get_low());
  a1 = Vec16f(tmp, a1.get_high());
}

// FLOAT 16 x 2
void transpose_reg(Vec16f& a0, Vec16f& a1)
{
  swap_halves(a0, a1);
}

// FLOAT 16 x 4
void transpose_reg(Vec16f& a0, Vec16f& a1, Vec16f& a2, Vec16f& a3)
{
  Vec16f b0,b1,b2,b3;
  b0 = blend16<0,1,2,3,16,17,18,19,8,9,10,11,24,25,26,27>(a0,a1);
  b1 = blend16<4,5,6,7,20,21,22,23,12,13,14,15,28,29,30,31>(a0,a1);
  b2 = blend16<0,1,2,3,16,17,18,19,8,9,10,11,24,25,26,27>(a2,a3);
  b3 = blend16<4,5,6,7,20,21,22,23,12,13,14,15,28,29,30,31>(a2,a3);
  swap_halves(b0,b2);
  swap_halves(b1,b3);
  a0 = b0;
  a1 = b1;
  a2 = b2;
  a3 = b3;
}

namespace impl
{
  /* A 4x8 transpose that behaves exactly like Vec4d's 4x4 transpose
   * on the lower and upper halves of the Vec8d
   */
  void _transpose4x16(Vec16f& a0, Vec16f& a1, Vec16f& a2, Vec16f& a3)
  {
    Vec16f b0,b1,b2,b3;
    b0 = blend16<0,1,16,17,4,5,20,21,8,9,24,25,12,13,28,29>(a0,a1);
    b1 = blend16<2,3,18,19,6,7,22,23,10,11,26,27,14,15,30,31>(a0,a1);
    b2 = blend16<0,1,16,17,4,5,20,21,8,9,24,25,12,13,28,29>(a2,a3);
    b3 = blend16<2,3,18,19,6,7,22,23,10,11,26,27,14,15,30,31>(a2,a3);
    a0 = blend16<0,1,2,3,16,17,18,19,8,9,10,11,24,25,26,27>(b0,b2);
    a1 = blend16<0,1,2,3,16,17,18,19,8,9,10,11,24,25,26,27>(b1,b3);
    a2 = blend16<4,5,6,7,20,21,22,23,12,13,14,15,28,29,30,31>(b0,b2);
    a3 = blend16<4,5,6,7,20,21,22,23,12,13,14,15,28,29,30,31>(b1,b3);
  }
}

// FLOAT 16 x 8
void transpose_reg(Vec16f& a0, Vec16f& a1, Vec16f& a2, Vec16f& a3,
		   Vec16f& a4, Vec16f& a5, Vec16f& a6, Vec16f& a7)
{
  impl::_transpose4x16(a0,a1,a2,a3);
  impl::_transpose4x16(a4,a5,a6,a7);
  swap_halves(a0,a4);
  swap_halves(a1,a5);
  swap_halves(a2,a6);
  swap_halves(a3,a7);
}

#endif

#endif
