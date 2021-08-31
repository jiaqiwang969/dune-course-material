# A CMake module to check for the existence of submodules!
#
# .. cmake_function:: dune_check_submodule
#
#    .. cmake_param:: PATH
#       :required:
#
#       The relative path to the submodule directory
#
#    .. cmake_param:: INDICATOR
#       :required:
#
#       A filename (like setup.py) that indicates a correctly cloned submodule
#


function(dune_check_submodule)
  # Parse Arguments
  include(CMakeParseArguments)
  cmake_parse_arguments(SUBMODULE "" "PATH;INDICATOR" "" ${ARGN})

  if(SUBMODULE_UNPARSED_ARGUMENTS)
    message(WARNING "Unparsed arguments in dune_check_submodule: This often indicates typos!")
  endif()

  if(NOT SUBMODULE_PATH)
    message(FATAL_ERROR "PATH argument not given to dune_check_submodule!")
  endif()
  if(NOT SUBMODULE_INDICATOR)
    message(FATAL_ERROR "INDICATOR argument not given to dune_check_submodule!")
  endif()

  if(NOT EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${SUBMODULE_PATH}/${SUBMODULE_INDICATOR})
    message(FATAL_ERROR "No git submodule found at location ${CMAKE_CURRENT_SOURCE_DIR}/${SUBMODULE_PATH}. You should clone this repository with the --recursive flag! It is described in the README!")
  endif()
endfunction()
