dune_symlink_to_source_files(FILES square.msh)

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_preconditioner_poisson_nn
        INIFILE poisson_nn.mini
        SOURCE poisson_nn_driver.cc
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_preconditioner_poisson_jacobi
        INIFILE poisson_jacobi.mini
        SOURCE poisson_jacobi_driver.cc
        )

dune_add_formcompiler_system_test(UFLFILE poisson.ufl
        BASENAME blockstructured_preconditioner_poisson_unstructured
        INIFILE poisson_unstructured.mini
        SOURCE poisson_unstructured_driver.cc
        )

dune_add_formcompiler_system_test(UFLFILE linear_elasticity.ufl
        BASENAME blockstructured_preconditioner_linear_elasticity_nn
        INIFILE linear_elasticity_nn.mini
        SOURCE linear_elasticity_nn_driver.cc
        )

dune_add_formcompiler_system_test(UFLFILE linear_elasticity.ufl
        BASENAME blockstructured_preconditioner_linear_elasticity_jacobi
        INIFILE linear_elasticity_jacobi.mini
        SOURCE linear_elasticity_jacobi_driver.cc
        )
