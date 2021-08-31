add_subdirectory(jacobi)
add_subdirectory(localsolver)
add_subdirectory(schur_complement)
add_subdirectory(two_level)

install(FILES preconditioner.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen/blockstructured/preconditioner/
        )
