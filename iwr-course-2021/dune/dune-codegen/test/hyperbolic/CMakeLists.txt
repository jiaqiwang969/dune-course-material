dune_add_formcompiler_system_test(UFLFILE lineartransport.ufl
                                  BASENAME lineartransport
                                  INIFILE lineartransport.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE linearacoustics.ufl
                                  BASENAME linearacoustics
                                  INIFILE linearacoustics.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE shallowwater.ufl
                                  BASENAME shallowwater
                                  INIFILE shallowwater.mini
                                  LABELS quick)
