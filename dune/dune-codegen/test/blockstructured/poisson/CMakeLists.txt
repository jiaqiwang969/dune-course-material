add_subdirectory(3d)


dune_symlink_to_source_files(FILES square.msh cube.msh)

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson
        INIFILE poisson.mini
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson_unstructured
        INIFILE poisson_unstructured.mini
        )

dune_add_formcompiler_system_test(UFLFILE poisson_tensor.ufl
        BASENAME blockstructured_poisson_tensor
        INIFILE poisson_tensor.mini
        )

dune_add_formcompiler_system_test(UFLFILE poisson_neumann.ufl
        BASENAME blockstructured_poisson_neumann
        INIFILE poisson_neumann.mini
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson_matrix_free
        INIFILE poisson_matrix_free.mini
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson_vec
        INIFILE poisson_vec.mini
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson_unstructured_vec
        INIFILE poisson_unstructured_vec.mini
        LABELS quick
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson_grid
        INIFILE poisson_grid.mini
)

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_poisson_vec_tail
        INIFILE poisson_vec_tail.mini
        )
