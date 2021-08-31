# File for module specific CMake tests.
#
# .. cmake_function:: dune_add_generated_executable
#
#    .. cmake_param:: UFLFILE
#       :single:
#       :required:
#
#       The UFL file to create the executable from.
#
#    .. cmake_param:: INIFILE
#       :single:
#       :required:
#
#       The ini file that controls the form compilation process.
#       It is expected to contain a [formcompiler] section
#
#    .. cmake_param:: TARGET
#       :single:
#       :required:
#
#       The name given to the added executable target.
#
#    .. cmake_param:: SOURCE
#       :single:
#
#       The cc source file to build from. If omitted, a minimal
#       source file and a driver file will be generated.
#
#    .. cmake_param:: FORM_COMPILER_ARGS
#       :multi:
#       :argname: arg
#
#       Additional arguments as recognized by the form compiler.
#
#    .. cmake_param:: DEPENDS
#       :multi:
#       :argname: dep
#
#       Additional dependencies of the generated executable (changes in those
#       will retrigger generation)
#
#    .. cmake_param:: EXCLUDE_FROM_ALL
#       :option:
#
#       Set this option, if you do not want the target to be automatically
#       built. This option is forwarded to the builtin command add_executable.
#
#    .. cmake_param:: ANALYZE_GRID
#       :option:
#
#       Set this option to enable code generation time grid analysis.
#       This is useful to reduce the variety of sum factorization kernels
#       in unstructured grids. Note that the grid analysis tool needs to
#       be able to construct your grid from the given inifile. If you have
#       a custom grid construction method, you can use ANALYZE_GRID_COMMAND
#       instead.
#
#    .. cmake_param:: ANALYZE_GRID_COMMAND
#       :multi:
#       :argname: command
#
#       Use this to pass a custom grid analysis command. This is necessary
#       if you use a custom grid generation methdod. The inifile and the
#       outputfile will be appended to this command. You can use the analysis code in
#       dune/codegen/sumfact/analyzegrid.hh to write your own tool.
#       Specifying this option will automatically set ANALYZE_GRID.
#
#
#    Add an executable to the project that gets automatically
#    generated at configure time with the form compiler uf2pdelab.
#    Regeneration is triggered correctly if the UFL file or the
#    form compiler changed.
#
# .. cmake_variable:: DUNE_CODEGEN_PROFILING
#
#    Set this variable from your opts file to enable statistic profiling of
#    the code generation process. This usually introduces additional cost.
#    A cProfile file for post processing will be written whenever the code
#    generator is run.
#

find_package(benchmark)

if (DUNE_CODEGEN_PROFILING)
  find_package(likwid)
endif()

add_custom_target(generation)

# Gather a list of form compiler sources to add as dependencies
# to have correct retriggers of generated executables
if(CMAKE_PROJECT_NAME STREQUAL dune-codegen)
  set(UFL2PDELAB_GLOB_PATTERN "${CMAKE_SOURCE_DIR}/python/*.py")
  set(dune-codegen_path ${CMAKE_SOURCE_DIR}/cmake/modules)
else()
  dune_module_path(MODULE dune-codegen
                   RESULT dune-codegen_path
                   CMAKE_MODULES)
  dune_execute_process(COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env python ${dune-codegen_path}/dune-codegen_sourcepath.py
                       OUTPUT_VARIABLE dune-codegen_source
                       OUTPUT_STRIP_TRAILING_WHITESPACE
                       )
  set(UFL2PDELAB_GLOB_PATTERN "${dune-codegen_source}/*.py")
endif()
file(GLOB_RECURSE UFL2PDELAB_SOURCES ${UFL2PDELAB_GLOB_PATTERN})

function(dune_add_generated_executable)
  set(OPTIONS EXCLUDE_FROM_ALL ANALYZE_GRID)
  set(SINGLE TARGET SOURCE UFLFILE INIFILE)
  set(MULTI FORM_COMPILER_ARGS DEPENDS ANALYZE_GRID_COMMAND)
  include(CMakeParseArguments)
  cmake_parse_arguments(GEN "${OPTIONS}" "${SINGLE}" "${MULTI}" ${ARGN})

  if(GEN_UNPARSED_ARGUMENTS)
    message(FATAL_ERROR "Unrecognized arguments in dune_add_generated_executable. This usually indicates a typo.")
  endif()

  set(MPI_OPTION "0")
  if(MPI_FOUND)
    set(MPI_OPTION "1")
  endif()

  # Apply defaults and enforce requirements
  if(NOT GEN_TARGET)
    message(FATAL_ERROR "Need to specify the TARGET parameter for dune_add_generated_executable")
  endif()
  if(NOT GEN_UFLFILE)
    message(FATAL_ERROR "Need to specify the UFLFILE parameter for dune_add_generated_executable")
  endif()
  if(NOT IS_ABSOLUTE ${GEN_UFLFILE})
    set(GEN_UFLFILE ${CMAKE_CURRENT_SOURCE_DIR}/${GEN_UFLFILE})
  endif()
  if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${GEN_INIFILE})
    set(GEN_INIFILE ${CMAKE_CURRENT_SOURCE_DIR}/${GEN_INIFILE})
  endif()
  if(NOT GEN_SOURCE)
    # Generate a driver file
    set(GEN_SOURCE ${GEN_TARGET}_driver.cc)
    add_custom_command(OUTPUT ${GEN_SOURCE}
                       COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env generate_driver
                               --uflfile ${GEN_UFLFILE}
                               --ini-file ${GEN_INIFILE}
                               --target-name ${GEN_TARGET}
                               --driver-file ${GEN_SOURCE}
                               --project-basedir ${CMAKE_BINARY_DIR}
                               --with-mpi ${MPI_OPTION}
                               ${GEN_FORM_COMPILER_ARGS}
                       DEPENDS ${GEN_UFLFILE} ${UFL2PDELAB_SOURCES} ${GEN_DEPENDS} ${DUNE_CODEGEN_ADDITIONAL_PYTHON_SOURCES}
                       COMMENT "Generating driver for the target ${GEN_TARGET}"
                       )
  endif()
  if(GEN_EXCLUDE_FROM_ALL)
    set(GEN_EXCLUDE_FROM_ALL "EXCLUDE_FROM_ALL")
  else()
    set(GEN_EXCLUDE_FROM_ALL "")
  endif()
  if(GEN_ANALYZE_GRID_COMMAND)
    set(GEN_ANALYZE_GRID 1)
  else()
    dune_module_path(MODULE dune-codegen RESULT codegenbin BUILD_DIR)
    set(GEN_ANALYZE_GRID_COMMAND ${codegenbin}/bin/analyzegrid/analyze_grid)
  endif()

  # Process analyze grid option
  set(ANALYZE_GRID_FILE)
  set(ANALYZE_GRID_OPTION)
  if(GEN_ANALYZE_GRID)
    if(NOT consistent-edge-orientation_FOUND)
      message(FATAL_ERROR "Asked for grid analysis, but the module consistent-edge-orientation was not found!")
    endif()
    set(ANALYZE_GRID_FILE "${CMAKE_CURRENT_BINARY_DIR}/${GEN_TARGET}.csv")
    set(ANALYZE_GRID_OPTION "--grid-info=${ANALYZE_GRID_FILE}")
    add_custom_command(OUTPUT ${ANALYZE_GRID_FILE}
                       COMMAND ${GEN_ANALYZE_GRID_COMMAND} ${GEN_INIFILE} ${ANALYZE_GRID_FILE}
                       COMMENT "Analyzing the grid for target ${GEN_TARGET}..."
                       )
  endif()

  if(DUNE_CODEGEN_PROFILING)
    # This is a bit silly, but cProfile only finds entry point scripts
    # if their full path is provided.
    set(fullcommand "${DUNE_PYTHON_VIRTUALENV_PATH}/bin/generate_operators")
  endif()

  # Parse a mapping of operators to build and their respective filenames
  dune_execute_process(COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env python ${dune-codegen_path}/deplist.py ${GEN_INIFILE} ${GEN_TARGET} ${CMAKE_CURRENT_BINARY_DIR}/interface.log)
  parse_python_data(PREFIX depdata FILE ${CMAKE_CURRENT_BINARY_DIR}/interface.log)

  # Generate driver blocks
  set(header_deps)
  foreach(db ${depdata___driverblocks})
    add_custom_command(OUTPUT ${depdata___db${db}}
                       COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env generate_driver_block
                               --uflfile ${GEN_UFLFILE}
                               --ini-file ${GEN_INIFILE}
                               --target-name ${GEN_TARGET}
                               --driver-block-to-build ${db}
                               --driver-file ${GEN_SOURCE}
                               --project-basedir ${CMAKE_BINARY_DIR}
                               --with-mpi ${MPI_OPTION}
                               ${GEN_FORM_COMPILER_ARGS}
                       DEPENDS ${GEN_UFLFILE} ${UFL2PDELAB_SOURCES} ${GEN_DEPENDS} ${DUNE_CODEGEN_ADDITIONAL_PYTHON_SOURCES}
                       COMMENT "Generating driver block ${depdata___db${db}} for the target ${GEN_TARGET}"
                       )
    set(header_deps ${header_deps} ${depdata___db${db}})
  endforeach()


  # Define build rules for all operator header files and gather a list of them
  foreach(op ${depdata___operators})
    set(GENERATION_COMMAND generate_operators)
    if(DUNE_CODEGEN_PROFILING)
      set(GENERATION_COMMAND python -m cProfile -o ${depdata___${op}}.prof ${fullcommand})
    endif()

    add_custom_command(OUTPUT ${depdata___${op}}
                       COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env ${GENERATION_COMMAND}
                               --project-basedir ${CMAKE_BINARY_DIR}
                               ${GEN_FORM_COMPILER_ARGS}
                               --uflfile ${GEN_UFLFILE}
                               --ini-file ${GEN_INIFILE}
                               --target-name ${GEN_TARGET}
                               --operator-to-build ${op}
                               --with-mpi ${MPI_OPTION}
                               ${ANALYZE_GRID_OPTION}
                       DEPENDS ${GEN_UFLFILE} ${UFL2PDELAB_SOURCES} ${GEN_DEPENDS} ${DUNE_CODEGEN_ADDITIONAL_PYTHON_SOURCES} ${ANALYZE_GRID_FILE}
                       COMMENT "Generating operator file ${depdata___${op}} for the target ${GEN_TARGET}"
                       )
    set(header_deps ${header_deps} ${depdata___${op}})
  endforeach()

  add_executable(${GEN_TARGET} ${GEN_EXCLUDE_FROM_ALL} ${GEN_SOURCE} ${header_deps})
  target_include_directories(${GEN_TARGET} PUBLIC ${CMAKE_CURRENT_BINARY_DIR})
  add_dependencies(generation ${GEN_TARGET})
endfunction()

include(GeneratedSystemtests)
include(DuneSubmoduleChecker)
