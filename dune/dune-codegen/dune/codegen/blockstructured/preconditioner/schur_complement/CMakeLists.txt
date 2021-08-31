add_subdirectory(localoperator)

install(FILES
        decomposition.hh
        operator.hh
        preconditioner.hh
        solver.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen/blockstructured/preconditioner/schur_complement
        )
