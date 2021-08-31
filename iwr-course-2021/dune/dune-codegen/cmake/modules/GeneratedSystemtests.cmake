# System testing for generated executables. All ideas taken from dune-testtools.
#
# .. cmake_function:: dune_add_formcompiler_system_test
#
#    .. cmake_param:: UFLFILE
#       :single:
#       :required:
#
#       The UFL file to create the generate code from.
#
#    .. cmake_param:: INIFILE
#       :single:
#       :required:
#
#       The ini file that controls the form compilation process.
#       It is expected to contain a [formcompiler] section. This
#       file may contain meta ini annotations.
#
#    .. cmake_param:: BASENAME
#       :single:
#       :required:
#
#       The basename for the generated executables.
#
#    .. cmake_param:: SCRIPT
#       :single:
#
#       The python script that decides about test failure/success.
#       Defaults to a script that simply runs the program and checks
#       the exit code. More scripts to be found in dune-testtools.
#
#    .. cmake_param:: SOURCE
#       :single:
#
#       The cc source file to build from. If omitted, a minimal
#       source file and a driver file will be generated.
#
#    .. cmake_param:: CREATED_TARGETS
#       :single:
#
#       A variable name that should be filled with the list of generated
#       targets. This can be used to modify these later on.
#
#    .. cmake_param:: DEPENDS
#       :multi:
#       :argname: dep
#
#       Additional dependencies of the generated executable (changes in those
#       will retrigger generation)
#
#    .. cmake_param:: NO_TESTS
#       :option:
#
#       If given, code will be generated and built normally, but no tests will
#       be added to the test suite.
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

function(dune_add_formcompiler_system_test)
  # parse arguments
  set(OPTION DEBUG NO_TESTS ANALYZE_GRID)
  set(SINGLE INIFILE BASENAME SCRIPT UFLFILE SOURCE CREATED_TARGETS)
  set(MULTI DEPENDS ANALYZE_GRID_COMMAND LABELS)
  cmake_parse_arguments(SYSTEMTEST "${OPTION}" "${SINGLE}" "${MULTI}" ${ARGN})

  if(SYSTEMTEST_UNPARSED_ARGUMENTS)
    message(WARNING "dune_add_system_test: Encountered unparsed arguments: This often indicates typos in named arguments")
  endif()

  # Construct strings to pass options to other functions
  set(DEBUG "")
  if(SYSTEMTEST_DEBUG)
    set(DEBUG "DEBUG")
  endif()
  set(SOURCE "")
  if(SYSTEMTEST_SOURCE)
    set(SOURCE SOURCE ${SYSTEMTEST_SOURCE})
  endif()
  set(ANALYZE_GRID_STR "")
  if(SYSTEMTEST_ANALYZE_GRID)
    set(ANALYZE_GRID_STR "ANALYZE_GRID")
  endif()
  set(ANALYZE_GRID_COMMAND_STR "")
  if(SYSTEMTEST_ANALYZE_GRID_COMMAND)
    set(ANALYZE_GRID_COMMAND_STR "ANALYZE_GRID_COMMAND ${SYSTEMTEST_ANALYZE_GRID_COMMAND}")
  endif()

  dune_declare_test_label(LABELS ${SYSTEMTEST_LABELS})

  # set a default for the script. call_executable.py just calls the executable.
  # There, it is also possible to hook in things depending on the inifile
  if(NOT SYSTEMTEST_SCRIPT)
    set(SYSTEMTEST_SCRIPT dune_execute.py)
  endif()

  # we provide two signatures: either a source(s) is given or a target(s)
  if(NOT SYSTEMTEST_UFLFILE)
    message(FATAL_ERROR "UFLFILE must be given for dune_add_generated_system_test!")
  endif()

  get_filename_component(REALPATH_INIFILE ${SYSTEMTEST_INIFILE} REALPATH)

  # Configure a bogus file from the meta ini file. This is a trick to retrigger configuration on meta ini changes.
  configure_file(${REALPATH_INIFILE} ${CMAKE_CURRENT_BINARY_DIR}/tmp_${SYSTEMTEST_INIFILE})

  # expand the given meta ini file into the build tree
  execute_process(COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env dune_expand_metaini.py
                          --cmake
                          --ini ${REALPATH_INIFILE}
                          --dir ${CMAKE_CURRENT_BINARY_DIR}
                          --section formcompiler
                          --file ${CMAKE_CURRENT_BINARY_DIR}/interface.log
                          )
  parse_python_data(PREFIX INIINFO FILE ${CMAKE_CURRENT_BINARY_DIR}/interface.log)

  foreach(inifile ${INIINFO_names})
    if(${INIINFO_${inifile}_suffix} STREQUAL "__empty")
      set(tname ${SYSTEMTEST_BASENAME})
    else()
      set(tname ${SYSTEMTEST_BASENAME}_${INIINFO_${inifile}_suffix})
      if(NOT TARGET ${SYSTEMTEST_BASENAME})
        add_custom_target(${SYSTEMTEST_BASENAME})
      endif()
    endif()

    dune_add_generated_executable(TARGET ${tname}
                                  UFLFILE ${SYSTEMTEST_UFLFILE}
                                  INIFILE "${CMAKE_CURRENT_BINARY_DIR}/${inifile}"
                                  DEPENDS ${SYSTEMTEST_INIFILE} ${SYSTEMTEST_DEPENDS}
                                  EXCLUDE_FROM_ALL
                                  ${SOURCE}
                                  ${ANALYZE_GRID_STR}
                                  ${ANALYZE_GRID_COMMAND_STR}
                                  )

    # Enrich the target with preprocessor variables from the __static section
    # just the way that dune-testtools does.
    dune_execute_process(COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env dune_extract_static.py
                               --ini ${inifile}
                               --file ${CMAKE_CURRENT_BINARY_DIR}/interface.log
                         WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                         OUTPUT_VARIABLE output
                         ERROR_MESSAGE "Error extracting static info from ${inifile}")
    parse_python_data(PREFIX STAT FILE ${CMAKE_CURRENT_BINARY_DIR}/interface.log)

    foreach(config ${STAT___CONFIGS})
      foreach(cd ${STAT___STATIC_DATA})
        target_compile_definitions(${tname} PUBLIC "${cd}=${STAT_${config}_${cd}}")
      endforeach()
    endforeach()

    # Add dependency on the metatarget for this systemtest
    if(NOT ${INIINFO_${inifile}_suffix} STREQUAL "__empty")
      add_dependencies(${SYSTEMTEST_BASENAME} ${tname})
    endif()

    if(NOT ${SYSTEMTEST_NO_TESTS})
      # and have it depend on the metatarget build_tests
      add_dependencies(build_tests ${tname})
      foreach(label IN LISTS SYSTEMTEST_LABELS)
        add_dependencies(build_${label}_tests ${tname})
      endforeach()

      _add_test(NAME ${tname}
                COMMAND ${CMAKE_BINARY_DIR}/run-in-dune-env ${SYSTEMTEST_SCRIPT}
                --exec "$<TARGET_FILE_DIR:${tname}>/$<TARGET_FILE_NAME:${tname}>"
                --ini "${CMAKE_CURRENT_BINARY_DIR}/${inifile}"
                --source ${CMAKE_CURRENT_SOURCE_DIR}
                --mpi-exec "${MPIEXEC}"
                --mpi-numprocflag=${MPIEXEC_NUMPROC_FLAG}
                --mpi-preflags "${MPIEXEC_PREFLAGS}"
                --mpi-postflags "${MPIEXEC_POSTFLAGS}"
                --max-processors=${DUNE_MAX_TEST_CORES}
               )

      set_tests_properties(${tname} PROPERTIES SKIP_RETURN_CODE 77)
      set_tests_properties(${tname} PROPERTIES TIMEOUT 120)
      set_tests_properties(${tname} PROPERTIES LABELS "${SYSTEMTEST_LABELS}")
    endif()
  endforeach()
endfunction()
