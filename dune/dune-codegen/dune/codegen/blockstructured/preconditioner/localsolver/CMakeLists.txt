add_subdirectory(wrapper)

install(FILES iterative_local_solver.hh
              local_solver.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen/blockstructured/preconditioner/localsolver
        )
