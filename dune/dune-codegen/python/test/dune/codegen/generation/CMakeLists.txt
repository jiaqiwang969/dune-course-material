dune_python_add_test(NAME pytest
                     COMMAND ${DUNE_PYTHON_VIRTUALENV_EXECUTABLE} -m pytest --pep8
                     WORKING_DIRECTORY ${CMAKE_SOURCE_DIR}/python/test/dune/codegen/generation
                     )
