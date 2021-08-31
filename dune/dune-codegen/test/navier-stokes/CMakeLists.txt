add_subdirectory(reference_program)

dune_add_formcompiler_system_test(UFLFILE navierstokes_2d_dg_quadrilateral.ufl
                                  BASENAME navierstokes_2d_dg_quadrilateral
                                  INIFILE navierstokes_2d_dg_quadrilateral.mini
                                  SCRIPT dune_execute_parallel.py
                                  LABELS quick
                                  )

dune_add_formcompiler_system_test(UFLFILE navierstokes_3d_dg_quadrilateral.ufl
                                  BASENAME navierstokes_3d_dg_quadrilateral
                                  INIFILE navierstokes_3d_dg_quadrilateral.mini
                                  )
