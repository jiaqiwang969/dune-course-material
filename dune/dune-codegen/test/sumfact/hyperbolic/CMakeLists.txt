dune_add_formcompiler_system_test(UFLFILE lineartransport.ufl
                                  BASENAME sumfact_lineartransport
                                  INIFILE lineartransport.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE linearacoustics.ufl
                                  BASENAME sumfact_linearacoustics
                                  INIFILE linearacoustics.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE shallowwater.ufl
                                  BASENAME sumfact_shallowwater
                                  INIFILE shallowwater.mini
                                  LABELS quick)
