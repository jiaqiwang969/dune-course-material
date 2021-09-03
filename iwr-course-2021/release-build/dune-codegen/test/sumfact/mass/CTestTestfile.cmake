# CMake generated Testfile for 
# Source directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass
# Build directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(sumfact_mass_nonvec "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_nonvec" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_nonvec.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_mass_nonvec PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;2;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;0;")
add_test(sumfact_mass_vec "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_vec" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_vec.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_mass_vec PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;2;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;0;")
add_test(sumfact_mass_3d_nonvec "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_3d_nonvec" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_3d_nonvec.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_mass_3d_nonvec PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;7;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;0;")
add_test(sumfact_mass_3d_vec "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_3d_vec" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_3d_vec.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_mass_3d_vec PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;7;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;0;")
add_test(sumfact_mass_sliced "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/run-in-dune-env" "dune_execute.py" "--exec" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_sliced" "--ini" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/mass/sumfact_mass_sliced.ini" "--source" "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass" "--mpi-exec" "/opt/homebrew/bin/mpiexec" "--mpi-numprocflag=-n" "--mpi-preflags" "" "--mpi-postflags" "" "--max-processors=2")
set_tests_properties(sumfact_mass_sliced PROPERTIES  LABELS "" SKIP_RETURN_CODE "77" TIMEOUT "120" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/cmake/modules/GeneratedSystemtests.cmake;183;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;12;dune_add_formcompiler_system_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/mass/CMakeLists.txt;0;")