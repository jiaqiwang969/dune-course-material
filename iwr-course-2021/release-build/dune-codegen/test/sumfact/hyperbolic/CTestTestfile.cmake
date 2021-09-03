# CMake generated Testfile for 
# Source directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic
# Build directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(sumfact_lineartransport "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic/sumfact_lineartransport" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic/sumfact_lineartransport.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_lineartransport PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic/CMakeLists.txt;1;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic/CMakeLists.txt;0;")
add_test(sumfact_linearacoustics "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic/sumfact_linearacoustics" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic/sumfact_linearacoustics.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_linearacoustics PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic/CMakeLists.txt;6;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic/CMakeLists.txt;0;")
add_test(sumfact_shallowwater "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic/sumfact_shallowwater" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/hyperbolic/sumfact_shallowwater.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_shallowwater PROPERTIES  LABELS "quick" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic/CMakeLists.txt;11;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/hyperbolic/CMakeLists.txt;0;")
