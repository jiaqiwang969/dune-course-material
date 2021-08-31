#=====
# CG
#=====

dune_add_formcompiler_system_test(UFLFILE heatequation.ufl
                                  BASENAME heatequation
                                  INIFILE heatequation.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE heatequation_time_dependent_bc.ufl
                                  BASENAME heatequation_time_dependent_bc
                                  INIFILE heatequation_time_dependent_bc.mini
                                  LABELS quick)

#=====
# DG
#=====

dune_add_formcompiler_system_test(UFLFILE heatequation_dg.ufl
                                  BASENAME heatequation_dg
                                  INIFILE heatequation_dg.mini
                                  LABELS quick)

#====================
# Reference solutions
#====================

# Hand written reference solutions
add_executable(heatequation_implicit_ref heatequation_implicit_ref.cc)
dune_symlink_to_source_files(FILES heatequation_implicit_ref.ini)
set_target_properties(heatequation_implicit_ref PROPERTIES EXCLUDE_FROM_ALL 1)

add_executable(heatequation_explicit_ref heatequation_explicit_ref.cc)
set_target_properties(heatequation_explicit_ref PROPERTIES EXCLUDE_FROM_ALL 1)
