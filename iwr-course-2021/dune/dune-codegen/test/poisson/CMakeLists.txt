add_subdirectory(dimension-grid-variations)

# Symlink any reference solutions
dune_symlink_to_source_files(FILES poisson_ref.vtu
                                   poisson_dg_ref.vtu
                             )


# 1. Poisson Test Case: source f, bc g
dune_add_formcompiler_system_test(UFLFILE poisson.ufl
                                  BASENAME poisson
                                  INIFILE poisson.mini
                                  )

# 2. Poisson Test Case: source f, mixed neumann/dirichlet boundary
dune_add_formcompiler_system_test(UFLFILE poisson_neumann.ufl
                                  BASENAME poisson_neumann
                                  INIFILE poisson_neumann.mini
                                  LABELS quick
                                  )

# 3. Poisson Test Case: DG, f + pure dirichlet
dune_add_formcompiler_system_test(UFLFILE poisson_dg.ufl
                                  BASENAME poisson_dg
                                  INIFILE poisson_dg.mini
                                  )

# 4. Poisson Test Case: DG, mixed bc
dune_add_formcompiler_system_test(UFLFILE poisson_dg_neumann.ufl
                                  BASENAME poisson_dg_neumann
                                  INIFILE poisson_dg_neumann.mini
                                  LABELS quick
                                  )

# 5. Poisson Test Case: matrix free
dune_add_formcompiler_system_test(UFLFILE poisson.ufl
                                  BASENAME poisson_matrix_free
                                  INIFILE poisson_matrix_free.mini
                                  )

# 6. Poisson Test Case: DG, matrix free
# Note: Converges but is too slow due to bad solver.
dune_add_formcompiler_system_test(UFLFILE poisson_dg.ufl
                                  BASENAME poisson_dg_matrix_free
                                  INIFILE poisson_dg_matrix_free.mini
                                  )

# 8. Poisson with operator counting
if(dune-opcounter_FOUND)
  dune_add_formcompiler_system_test(UFLFILE opcount_poisson_dg.ufl
                                    BASENAME opcount_poisson_dg_symdiff
                                    INIFILE opcount_poisson_dg_symdiff.mini
                                    LABELS quick
                                    )
endif()

# 9. Poisson Test Case: DG quadrilaterals
dune_add_formcompiler_system_test(UFLFILE poisson_dg_quadrilateral.ufl
                                  BASENAME poisson_dg_quadrilateral
                                  INIFILE poisson_dg_quadrilateral.mini
                                  )

# 10. Poisson Test Case with a full permeability tensor
dune_add_formcompiler_system_test(UFLFILE poisson_tensor.ufl
                                  BASENAME poisson_tensor
                                  INIFILE poisson_tensor.mini
                                  LABELS quick
                                  )

# 11. Poisson Test Case: DG with full permeability tensor
dune_add_formcompiler_system_test(UFLFILE poisson_dg_tensor.ufl
                                  BASENAME poisson_dg_tensor
                                  INIFILE poisson_dg_tensor.mini
                                  LABELS quick
                                  )

# 12. Poisson Test Case with a custom function
dune_add_formcompiler_system_test(UFLFILE poisson_customfunction.ufl
                                  BASENAME poisson_customfunction
                                  INIFILE poisson_customfunction.mini
                                  LABELS quick
                                  )

# 13. Poisson Test Case: DG quadrilaterals with axiparallel mixin
dune_add_formcompiler_system_test(UFLFILE poisson_dg_quadrilateral.ufl
        BASENAME poisson_dg_axiparallel
        INIFILE poisson_dg_axiparallel.mini
        )


# the reference vtk file
add_executable(poisson_dg_ref reference_main.cc)
set_target_properties(poisson_dg_ref PROPERTIES EXCLUDE_FROM_ALL 1)
