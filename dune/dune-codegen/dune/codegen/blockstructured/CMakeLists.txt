add_subdirectory(preconditioner)

install(FILES blockstructuredqkfem.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen/blockstructured
        )
