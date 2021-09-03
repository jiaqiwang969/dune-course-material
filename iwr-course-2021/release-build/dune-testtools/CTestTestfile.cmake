# CMake generated Testfile for 
# Source directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools
# Build directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(pytest "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-python-env/bin/python" "-m" "pytest")
set_tests_properties(pytest PROPERTIES  WORKING_DIRECTORY "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/python" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/modules/DunePythonTestCommand.cmake;74;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/CMakeLists.txt;28;dune_python_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/CMakeLists.txt;0;")
add_test(pep8 "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-python-env/bin/python" "-m" "pytest" "--pep8")
set_tests_properties(pep8 PROPERTIES  WORKING_DIRECTORY "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/python" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/modules/DunePythonTestCommand.cmake;74;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/CMakeLists.txt;32;dune_python_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/CMakeLists.txt;0;")
subdirs("dune")
subdirs("doc")
subdirs("cmake")
