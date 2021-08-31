# Check that the submodules have been checked out!
dune_check_submodule(PATH pytools INDICATOR setup.py)
dune_check_submodule(PATH cgen INDICATOR setup.py)
dune_check_submodule(PATH pymbolic INDICATOR setup.py)
dune_check_submodule(PATH loopy INDICATOR setup.py)
dune_check_submodule(PATH ufl INDICATOR setup.py)

# Install all the external packages that we have as submodules
dune_python_install_package(PATH pytools)
dune_python_install_package(PATH cgen)
dune_python_install_package(PATH pymbolic)
dune_python_install_package(PATH loopy)
dune_python_install_package(PATH ufl)

# Install our python package
dune_python_install_package(PATH .)

if (${dune-common_VERSION} GREATER 2.7.0)
    dune_python_add_test(NAME pep8-ourcode
                         COMMAND ${DUNE_PYTHON_VIRTUALENV_EXECUTABLE} -m pytest --pep8 ${CMAKE_SOURCE_DIR}/python/dune/codegen
                         LABELS quick
                         )
endif ()

add_subdirectory(test)

add_executable(_autotune_target EXCLUDE_FROM_ALL _autotune.cc)
target_compile_options(_autotune_target PUBLIC -fno-strict-aliasing)

find_package(Threads)
if(benchmark_FOUND AND Threads_FOUND)
  target_link_libraries(_autotune_target benchmark Threads::Threads)
endif()
