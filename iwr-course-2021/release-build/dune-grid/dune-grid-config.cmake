if(NOT dune-grid_FOUND)
# Whether this module is installed or not
set(dune-grid_INSTALLED OFF)

# Settings specific to the module

# Package initialization
# Set prefix to source dir
set(PACKAGE_PREFIX_DIR /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid)
macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

#report other information
set_and_check(dune-grid_PREFIX "${PACKAGE_PREFIX_DIR}")
set_and_check(dune-grid_INCLUDE_DIRS "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid")
set(dune-grid_CXX_FLAGS "-std=c++17 -Wall -DDUNE_AVOID_CAPABILITIES_IS_PARALLEL_DEPRECATION_WARNING")
set(dune-grid_CXX_FLAGS_DEBUG "-g")
set(dune-grid_CXX_FLAGS_MINSIZEREL "-Os -DNDEBUG")
set(dune-grid_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -g0 -funroll-loops")
set(dune-grid_CXX_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG")
set(dune-grid_DEPENDS "dune-geometry (>= 2.7)")
set(dune-grid_SUGGESTS "dune-uggrid (>=2.7)")
set(dune-grid_MODULE_PATH "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/cmake/modules")
set(dune-grid_LIBRARIES "dunegrid")

# Lines that are set by the CMake build system via the variable DUNE_CUSTOM_PKG_CONFIG_SECTION
#Export the directory with the grid example for downstream modules
set(DUNE_GRID_EXAMPLE_GRIDS_PATH "/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/doc/grids/")


#import the target
if(dune-grid_LIBRARIES)
  get_filename_component(_dir "${CMAKE_CURRENT_LIST_FILE}" PATH)
  include("${_dir}/dune-grid-targets.cmake")
endif()
endif()
