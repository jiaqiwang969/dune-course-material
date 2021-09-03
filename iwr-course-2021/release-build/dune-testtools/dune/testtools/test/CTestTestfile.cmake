# CMake generated Testfile for 
# Source directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test
# Build directory: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(outputtreetest "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/outputtreetest")
set_tests_properties(outputtreetest PROPERTIES  LABELS "" PROCESSORS "1" REQUIRED_FILES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/outputtreetest" SKIP_RETURN_CODE "77" TIMEOUT "300" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/modules/DuneTestMacros.cmake;397;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/CMakeLists.txt;14;dune_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/CMakeLists.txt;0;")
add_test(triggertest "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/triggertest")
set_tests_properties(triggertest PROPERTIES  LABELS "" PROCESSORS "1" REQUIRED_FILES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/triggertest" SKIP_RETURN_CODE "77" TIMEOUT "300" _BACKTRACE_TRIPLES "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/modules/DuneTestMacros.cmake;397;_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/CMakeLists.txt;17;dune_add_test;/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/CMakeLists.txt;0;")
subdirs("constructiontest")
subdirs("cmakediscard")
subdirs("cmakepython")
subdirs("staticvariants")
subdirs("dynamicvariants")
subdirs("onemacrodynamicvariants")
subdirs("allvariants")
subdirs("parallel")
subdirs("convergencetest")
subdirs("outputcompare")
subdirs("vtkcompare")
subdirs("notestexpansion")
