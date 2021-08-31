# .. cmake_module::
#
#    Module that checks whether likwid is available and usable.
#
#    Variables used by this module which you may want to set:
#
#    :ref:`likwid_ROOT`
#       Path list to search for likwid.
#
#    Sets the following variables:
#
#    :code:`likwid_FOUND`
#       True if likwid available.
#
#    :code:`likwid_INCLUDE_DIRS`
#       Path to the likwid include directories.
#
#
#    :code:`likwid_LIBRARIES`
#       Link against these libraries to use likwid.
#
# .. cmake_variable:: likwid_ROOT
#
#    You may set this variable to have :ref:`Findlikwid` look
#    for the likwid package in the given paths before inspecting
#    system paths.
#
find_path(LIKWID_INCLUDE_DIR
        NAMES "likwid.h"
        PATHS ${likwid_ROOT}
        PATH_SUFFIXES "include" "include/likwid"
        NO_DEFAULT_PATH)
find_path(LIKWID_INCLUDE_DIR
        NAMES "likwid.h"
        PATH_SUFFIXES "include" "include/likwid")

find_library(LIKWID_LIBRARY
        NAMES "likwid"
        PATHS ${likwid_ROOT}
        PATH_SUFFIXES "lib" "lib32" "lib64"
        NO_DEFAULT_PATH)
find_library(LIKWID_LIBRARY
        NAMES "likwid"
        PATH_SUFFIXES "lib" "lib32" "lib64")

include(CMakePushCheckState)
cmake_push_check_state()

if(LIKWID_INCLUDE_DIR)
    set(CMAKE_REQUIRED_INCLUDES ${CMAKE_REQUIRED_INCLUDES} ${LIKWID_INCLUDE_DIR})
endif()
if(LIKWID_LIBRARY)
    set(CMAKE_REQUIRED_LIBRARIES ${CMAKE_REQUIRED_LIBRARIES} ${LIKWID_LIBRARY})
endif()

cmake_pop_check_state()

include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(
        "likwid"
        DEFAULT_MSG
        LIKWID_INCLUDE_DIR
        LIKWID_LIBRARY
)

mark_as_advanced(LIKWID_INCLUDE_DIR LIKWID_LIBRARY)

# if headers are found, store results
if(likwid_FOUND)
    set(likwid_INCLUDE_DIRS ${LIKWID_INCLUDE_DIR})
    set(likwid_LIBRARIES ${LIKWID_LIBRARY})
    # log result
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeOutput.log
            "Determing location of likwid succeeded:\n"
            "Include directory: ${likwid_INCLUDE_DIRS}\n"
            "Libraries to link against: ${likwid_LIBRARIES}\n\n")

    set(likwid_DUNE_COMPILE_FLAGS "-I${likwid_INCLUDE_DIRS}"
            CACHE STRING "Compile Flags used by DUNE when compiling with likwid programs")
    set(likwid_DUNE_LIBRARIES ${likwid_LIBRARIES}
            CACHE STRING "Libraries used by DUNE when linking likwid programs")
else()
    # log errornous result
    file(APPEND ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeError.log
            "Determing location of likwid failed:\n"
            "Include directory: ${likwid_INCLUDE_DIRS}\n"
            "Libraries to link against: ${likwid_LIBRARIES}\n\n")
endif()

# set HAVE_LIKWID for config.h
set(HAVE_LIKWID ${likwid_FOUND})


# register all likwid related flags
if(likwid_FOUND)
    dune_register_package_flags(COMPILE_DEFINITIONS "ENABLE_LIKWID=1"
            LIBRARIES "${likwid_LIBRARIES}"
            INCLUDE_DIRS "${likwid_INCLUDE_DIRS}")
endif()

# text for feature summary
set_package_properties("LIKWID" PROPERTIES
        DESCRIPTION "likwid"
        PURPOSE "Performance monitoring and benchmarking suite.")