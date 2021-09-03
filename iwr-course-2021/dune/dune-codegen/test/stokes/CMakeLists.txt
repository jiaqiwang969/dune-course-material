dune_symlink_to_source_files(FILES hagenpoiseuille_ref.vtu
                                   hagenpoiseuille_dg_ref.vtu
                             )

dune_add_formcompiler_system_test(UFLFILE stokes.ufl
                                  BASENAME stokes
                                  INIFILE stokes.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_quadrilateral.ufl
                                  BASENAME stokes_quadrilateral
                                  INIFILE stokes_quadrilateral.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_3d_quadrilateral.ufl
                                  BASENAME stokes_3d_quadrilateral
                                  INIFILE stokes_3d_quadrilateral.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_sym.ufl
                                  BASENAME stokes_sym
                                  INIFILE stokes_sym.mini
                                  LABELS quick
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_dg.ufl
                                  BASENAME stokes_dg
                                  INIFILE stokes_dg.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_dg_quadrilateral.ufl
                                  BASENAME stokes_dg_quadrilateral
                                  INIFILE stokes_dg_quadrilateral.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE stokes_3d_dg_quadrilateral.ufl
                                  BASENAME stokes_3d_dg_quadrilateral
                                  INIFILE stokes_3d_dg_quadrilateral.mini
                                  LABELS quick
                                  )

#dune_add_formcompiler_system_test(UFLFILE stokes_stress.ufl
#                                  BASENAME stokes_stress
#                                  INIFILE stokes_stress.mini
#                                  )

# Do not test stokes_stress_sym until the function_view project
# has been fully implemented.
#
#dune_add_formcompiler_system_test(UFLFILE stokes_stress_sym.ufl
#                                  BASENAME stokes_stress_sym
#                                  INIFILE stokes_stress_sym.mini
#                                  )
