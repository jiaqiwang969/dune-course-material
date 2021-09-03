if(NOT dune-testtools_FOUND)
# Whether this module is installed or not
set(dune-testtools_INSTALLED OFF)

# Settings specific to the module

# Package initialization
# Set prefix to source dir
set(PACKAGE_PREFIX_DIR /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools)
macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

#report other information
set_and_check(dune-testtools_PREFIX "${PACKAGE_PREFIX_DIR}")
set_and_check(dune-testtools_INCLUDE_DIRS "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools")
set(dune-testtools_CXX_FLAGS "-std=c++17 -Wall -DDUNE_AVOID_CAPABILITIES_IS_PARALLEL_DEPRECATION_WARNING")
set(dune-testtools_CXX_FLAGS_DEBUG "-g")
set(dune-testtools_CXX_FLAGS_MINSIZEREL "-Os -DNDEBUG")
set(dune-testtools_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -g0 -funroll-loops")
set(dune-testtools_CXX_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG")
set(dune-testtools_DEPENDS "dune-common")
set(dune-testtools_SUGGESTS "dune-grid;dune-alugrid")
set(dune-testtools_MODULE_PATH "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/cmake/modules")
set(dune-testtools_LIBRARIES "")

# Lines that are set by the CMake build system via the variable DUNE_CUSTOM_PKG_CONFIG_SECTION

set(DUNE_TESTTOOLS_PATH "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools")


#import the target
if(dune-testtools_LIBRARIES)
  get_filename_component(_dir "${CMAKE_CURRENT_LIST_FILE}" PATH)
  include("${_dir}/dune-testtools-targets.cmake")
endif()
endif()
