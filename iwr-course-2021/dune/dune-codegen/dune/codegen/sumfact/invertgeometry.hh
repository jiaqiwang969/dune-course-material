#ifndef DUNE_CODEGEN_SUMFACT_INVERTGEOMETRY_HH
#define DUNE_CODEGEN_SUMFACT_INVERTGEOMETRY_HH


template<typename T>
inline T invert_and_return_determinant(const T a00, const T a10, const T a01, const T a11, T inverse[4]){
  T det = a00 * a11 - a10 * a01;
  assert (std::abs(det) > 1e-12);

  inverse[0] = a11 / det;
  inverse[1] = -a10 / det;
  inverse[2] = -a01 / det;
  inverse[3] = a00 / det;

  return std::abs(det);
}


template<typename T>
inline T invert_and_return_determinant(const T a00, const T a10, const T a20,
                                       const T a01, const T a11, const T a21,
                                       const T a02, const T a12, const T a22,
                                       T inverse[9]){
  T t4 = a00 * a11;
  T t6 = a00 * a12;
  T t8  = a01 * a10;
  T t10 = a02 * a10;
  T t12 = a01 * a20;
  T t14 = a02 * a20;

  T det = t4 * a22;
  det -= t6 * a21;
  det -= t8 * a22;
  det += t10 * a21;
  det += t12 * a12;
  det -= t14 * a11;

  assert (std::abs(det) > 1e-12);

  T t17 = 1.0/det;

  inverse[0] = a11 * a22;
  inverse[0] -= a12 * a21;
  inverse[0] *= t17;

  inverse[3] = a02 * a21;
  inverse[3] -= a01 * a22;
  inverse[3] *= t17;

  inverse[6] = a01 * a12;
  inverse[6] -= a02 * a11;
  inverse[6] *= t17;

  inverse[1] = a12 * a20;
  inverse[1] -= a10 * a22;
  inverse[1] *= t17;

  inverse[4] = -t14;
  inverse[4] += a00 * a22;
  inverse[4] *= t17;

  inverse[7] = t10 - t6;
  inverse[7] *= t17;

  inverse[2] = a10 * a21;
  inverse[2] -= a11 * a20;
  inverse[2] *= t17;

  inverse[5] = t12;
  inverse[5] -= a00 * a21;
  inverse[5] *= t17;

  inverse[8] = t4 - t8;
  inverse[8] *= t17;

  return std::abs(det);
}


#endif
