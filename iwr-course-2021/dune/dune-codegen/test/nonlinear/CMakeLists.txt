dune_add_formcompiler_system_test(UFLFILE nonlinear.ufl
                                  BASENAME nonlinear
                                  INIFILE nonlinear.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE nonlinear_dg.ufl
                                  BASENAME nonlinear_dg
                                  INIFILE nonlinear_dg.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE nonlinear.ufl
                                  BASENAME nonlinear_matrix_free
                                  INIFILE nonlinear_matrix_free.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE nonlinear_dg.ufl
                                  BASENAME nonlinear_dg_matrix_free
                                  INIFILE nonlinear_dg_matrix_free.mini
                                  LABELS quick
                                  )


# Add the reference code with the PDELab localoperator that produced
# the reference vtk file
add_executable(nonlinear_ref reference_main.cc)
set_target_properties(nonlinear_ref PROPERTIES EXCLUDE_FROM_ALL 1)

dune_add_formcompiler_system_test(UFLFILE diffusivewave.ufl
                                  BASENAME diffusivewave
                                  INIFILE diffusivewave.mini
                                  LABELS quick)
