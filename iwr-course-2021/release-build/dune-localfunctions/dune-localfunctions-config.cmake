if(NOT dune-localfunctions_FOUND)
# Whether this module is installed or not
set(dune-localfunctions_INSTALLED OFF)

# Settings specific to the module

# Package initialization
# Set prefix to source dir
set(PACKAGE_PREFIX_DIR /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions)
macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

#report other information
set_and_check(dune-localfunctions_PREFIX "${PACKAGE_PREFIX_DIR}")
set_and_check(dune-localfunctions_INCLUDE_DIRS "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions")
set(dune-localfunctions_CXX_FLAGS "-std=c++17 -Wall -DDUNE_AVOID_CAPABILITIES_IS_PARALLEL_DEPRECATION_WARNING")
set(dune-localfunctions_CXX_FLAGS_DEBUG "-g")
set(dune-localfunctions_CXX_FLAGS_MINSIZEREL "-Os -DNDEBUG")
set(dune-localfunctions_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -g0 -funroll-loops")
set(dune-localfunctions_CXX_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG")
set(dune-localfunctions_DEPENDS "dune-geometry (>= 2.7)")
set(dune-localfunctions_SUGGESTS "")
set(dune-localfunctions_MODULE_PATH "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/cmake/modules")
set(dune-localfunctions_LIBRARIES "")

# Lines that are set by the CMake build system via the variable DUNE_CUSTOM_PKG_CONFIG_SECTION


#import the target
if(dune-localfunctions_LIBRARIES)
  get_filename_component(_dir "${CMAKE_CURRENT_LIST_FILE}" PATH)
  include("${_dir}/dune-localfunctions-targets.cmake")
endif()
endif()
