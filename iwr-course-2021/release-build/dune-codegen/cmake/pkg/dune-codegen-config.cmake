if(NOT dune-codegen_FOUND)
# Whether this module is installed or not
set(dune-codegen_INSTALLED ON)

# Settings specific to the module

# Package initialization

####### Expanded from @PACKAGE_INIT@ by configure_package_config_file() #######
####### Any changes to this file will be overwritten by the next CMake run ####
####### The input file was dune-codegen-config.cmake.in                            ########

get_filename_component(PACKAGE_PREFIX_DIR "${CMAKE_CURRENT_LIST_DIR}/../../../" ABSOLUTE)

macro(set_and_check _var _file)
  set(${_var} "${_file}")
  if(NOT EXISTS "${_file}")
    message(FATAL_ERROR "File or directory ${_file} referenced by variable ${_var} does not exist !")
  endif()
endmacro()

macro(check_required_components _NAME)
  foreach(comp ${${_NAME}_FIND_COMPONENTS})
    if(NOT ${_NAME}_${comp}_FOUND)
      if(${_NAME}_FIND_REQUIRED_${comp})
        set(${_NAME}_FOUND FALSE)
      endif()
    endif()
  endforeach()
endmacro()

####################################################################################

#report other information
set_and_check(dune-codegen_PREFIX "${PACKAGE_PREFIX_DIR}")
set_and_check(dune-codegen_INCLUDE_DIRS "${PACKAGE_PREFIX_DIR}/include")
set(dune-codegen_CXX_FLAGS "-std=c++17 -Wall -DDUNE_AVOID_CAPABILITIES_IS_PARALLEL_DEPRECATION_WARNING -DDUNE_ISTL_SUPPORT_OLD_CATEGORY_INTERFACE=1")
set(dune-codegen_CXX_FLAGS_DEBUG "-g")
set(dune-codegen_CXX_FLAGS_MINSIZEREL "-Os -DNDEBUG")
set(dune-codegen_CXX_FLAGS_RELEASE "-O3 -DNDEBUG -g0 -funroll-loops")
set(dune-codegen_CXX_FLAGS_RELWITHDEBINFO "-O2 -g -DNDEBUG")
set(dune-codegen_DEPENDS "dune-testtools;dune-pdelab;dune-alugrid")
set(dune-codegen_SUGGESTS "dune-opcounter;dune-uggrid;consistent-edge-orientation")
set(dune-codegen_MODULE_PATH "${PACKAGE_PREFIX_DIR}/share/dune/cmake/modules")
set(dune-codegen_LIBRARIES "dunecodegen")

# Lines that are set by the CMake build system via the variable DUNE_CUSTOM_PKG_CONFIG_SECTION


#import the target
if(dune-codegen_LIBRARIES)
  get_filename_component(_dir "${CMAKE_CURRENT_LIST_FILE}" PATH)
  include("${_dir}/dune-codegen-targets.cmake")
endif()
endif()
