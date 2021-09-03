# CMake generated Testfile for 
# Source directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval
# Build directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/coeffeval
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(coeffeval_poisson_grad "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/coeffeval/coeffeval_poisson_grad" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/coeffeval/coeffeval_poisson_grad.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(coeffeval_poisson_grad PROPERTIES  LABELS "quick" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval/CMakeLists.txt;1;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval/CMakeLists.txt;0;")
add_test(coeffeval_poisson_nongrad "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/coeffeval/coeffeval_poisson_nongrad" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/coeffeval/coeffeval_poisson_nongrad.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(coeffeval_poisson_nongrad PROPERTIES  LABELS "quick" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval/CMakeLists.txt;1;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/coeffeval/CMakeLists.txt;0;")