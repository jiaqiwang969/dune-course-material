#include "config.h"

#define MAX_VECTOR_SIZE 512

#include<dune/codegen/common/vectorclass.hh>
#include<dune/codegen/sumfact/transposereg.hh>

#include<array>
#include<iostream>
#include<utility>


template<std::size_t ...S>
void apply_function(std::array<VECTYPE, _M>& data, std::index_sequence<S...>)
{
  transpose_reg(std::get<S>(data) ...);
}


void print(const std::array<VECTYPE, _M>& data)
{
  for(int i=0; i<_M; ++i)
  {
    for(int j=0; j<_N; ++j)
      std::cout << data[i].extract(j) << " ";
    std::cout << std::endl;
  }
}


int main()
{
  // Setup data
  std::array<VECTYPE, _M> testdata;
  int data = 0;
  for(int i=0; i<_M; ++i)
    for(int j=0; j<_N; ++j, ++data)
      testdata[i].insert(j, data);

  std::array<VECTYPE, _M> originaldata(testdata);

  // Print the test data once
  std::cout << "Before transposition:" << std::endl;
  print(testdata);

  // Apply the transpose function
  apply_function(testdata, std::make_index_sequence<_M>{});

  // And print the test data once more
  std::cout << "After transposition:" << std::endl;
  print(testdata);

  int result = 0;
  for(int i=0; i<_M; ++i)
    for(int j=0; j<_N; ++j)
    {
      // Dirty handcoding of the generic permutation
      auto NM = (int)_N / (int)_M;
      auto linear = i * _N + j;
      auto block = linear / NM;
      auto newblock = (block % _M) * _M + (block / _M);
      auto newlinear = newblock * NM + (linear % NM);
      auto newj = newlinear % _N;
      auto newi = newlinear / _N;

      if(testdata[newi].extract(newj) != originaldata[i].extract(j))
      {
	std::cout << "Test failure in transpose: index (" << i << "," << j << ") in original data does not match index (" << newi << "," << newj << ") in new data." << std::endl;
	++result;
      }
    }

  return result;
}
