dune_add_formcompiler_system_test(UFLFILE stokes.ufl
                                  BASENAME sumfact_stokes
                                  INIFILE stokes.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_dg.ufl
                                  BASENAME sumfact_stokes_dg
                                  INIFILE stokes_dg.mini
                                  LABELS quick
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_3d_dg.ufl
                                  BASENAME sumfact_stokes_3d_dg
                                  INIFILE stokes_3d_dg.mini
                                  )
