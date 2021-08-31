# There is a clang bug for a 16x8 transpose and I did not manage to include
# only that one due to a weirdness in CI - it worked on my machine through testtools.
if(NOT("${CMAKE_CXX_COMPILER_ID}" STREQUAL "Clang"))
  dune_add_system_test(SOURCE test_transpose.cc
                       BASENAME test_transpose
                       INIFILE transpose.mini
                       )
endif()
