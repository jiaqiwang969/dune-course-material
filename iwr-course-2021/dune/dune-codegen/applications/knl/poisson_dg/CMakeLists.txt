dune_add_formcompiler_system_test(UFLFILE poisson_dg.ufl
                                  BASENAME app_knl_poisson
                                  INIFILE knl_poisson_dg.mini
                                  NO_TESTS
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_dg.ufl
                                  BASENAME verify_app_knl_poisson_dg
                                  INIFILE verify.mini
                                  NO_TESTS
                                  )
