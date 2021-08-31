dune_add_formcompiler_system_test(UFLFILE poisson_dg_tensor.ufl
                                  BASENAME app_knl_poisson_tensor
                                  INIFILE knl_poisson_dg_tensor.mini
                                  NO_TESTS
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_dg_tensor.ufl
                                  BASENAME verify_app_knl_poisson_dg_tensor
                                  INIFILE verify.mini
                                  NO_TESTS
                                  )
