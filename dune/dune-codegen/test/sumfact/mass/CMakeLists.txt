# A mass matrix test: Simplest possible example
dune_add_formcompiler_system_test(UFLFILE mass.ufl
                                  BASENAME sumfact_mass
                                  INIFILE mass.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE mass_3d.ufl
                                  BASENAME sumfact_mass_3d
                                  INIFILE mass_3d.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE mass_3d.ufl
                                  BASENAME sumfact_mass_sliced
                                  INIFILE sliced.mini
                                  )
