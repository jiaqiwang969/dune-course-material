#include<iostream>

int main()
{
  std::cout << "This test was skipped because it failed the following CMake Conditions:" << std::endl;
  std::cout << "  SuiteSparse_UMFPACK_FOUND" << std::endl;
std::cout << "  ARPACKPP_FOUND" << std::endl;

  return 77;
}
