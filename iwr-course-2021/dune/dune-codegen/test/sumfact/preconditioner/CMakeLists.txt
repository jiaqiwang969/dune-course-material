dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                  BASENAME sumfact_preconditioner_2d
                                  INIFILE preconditioner_2d.mini
                                  SOURCE test_preconditioner_2d.cc
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_preconditioner_3d
                                  INIFILE preconditioner_3d.mini
                                  SOURCE test_preconditioner_3d.cc
                                  LABELS quick
                                  )
