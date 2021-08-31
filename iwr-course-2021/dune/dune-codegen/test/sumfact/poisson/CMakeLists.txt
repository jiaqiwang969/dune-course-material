add_subdirectory(facedir-facemod-variation)

#====================
# Poisson CG in 2D/3D
#====================
dune_add_formcompiler_system_test(UFLFILE poisson_2d.ufl
                                  BASENAME sumfact_poisson_2d
                                  INIFILE poisson_2d.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_3d.ufl
                                  BASENAME sumfact_poisson_3d
                                  INIFILE poisson_3d.mini
                                  )

#================
# Opcounter tests
#================
dune_add_formcompiler_system_test(UFLFILE poisson_2d.ufl
                                  BASENAME opcount_sumfact_poisson_2d_order2
                                  INIFILE opcount_poisson_2d_order2.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                  BASENAME opcount_sumfact_poisson_dg_2d_vec
                                  INIFILE opcount_sumfact_poisson_dg_2d_vec.mini
                                  )

#====================
# Poisson DG in 2D/3D
#====================
dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                  BASENAME sumfact_poisson_dg_2d
                                  INIFILE poisson_dg_2d.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_poisson_dg_3d
                                  INIFILE poisson_dg_3d.mini
                                  )


#===============================
# Poisson on 'unstructured grid'
#===============================
dune_add_formcompiler_system_test(UFLFILE poisson_2d.ufl
                                  BASENAME sumfact_poisson_2d_unstructured
                                  INIFILE poisson_2d_unstructured.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_3d.ufl
                                  BASENAME sumfact_poisson_3d_unstructured
                                  INIFILE poisson_3d_unstructured.mini
                                  )

#==================================
# Poisson DG on 'unstructured grid'
#==================================
if(consistent-edge-orientation_FOUND)
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                    BASENAME sumfact_poisson_dg_2d_unstructured
                                    INIFILE poisson_dg_2d_unstructured.mini
                                    ANALYZE_GRID
                                    )
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                    BASENAME sumfact_poisson_dg_3d_unstructured
                                    INIFILE poisson_dg_3d_unstructured.mini
                                    ANALYZE_GRID
                                    )
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                    BASENAME sumfact_poisson_dg_2d_gmsh
                                    INIFILE poisson_dg_2d_gmsh.mini
                                    ANALYZE_GRID
                                    LABELS quick)
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                    BASENAME sumfact_poisson_dg_3d_gmsh
                                    INIFILE poisson_dg_3d_gmsh.mini
                                    ANALYZE_GRID
                                    LABELS quick)
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                    BASENAME sumfact_poisson_fastdg_2d_gmsh
                                    INIFILE poisson_fastdg_2d_gmsh.mini
                                    ANALYZE_GRID
                                    )
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                    BASENAME sumfact_poisson_fastdg_3d_gmsh
                                    INIFILE poisson_fastdg_3d_gmsh.mini
                                    ANALYZE_GRID
                                    )
  dune_symlink_to_source_files(FILES square_quad.msh)
  dune_symlink_to_source_files(FILES cube_hexa_2.msh)
  dune_symlink_to_source_files(FILES cube_hexa.msh)
endif()

#=============================================
# Poisson DG using FastDGGridOperator in 2D/3D
#=============================================
dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                  BASENAME sumfact_poisson_fastdg_2d
                                  INIFILE poisson_fastdg_2d.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_poisson_fastdg_3d
                                  INIFILE poisson_fastdg_3d.mini
                                  )

#================================
# 'Poisson' DG with a full tensor
#================================
dune_add_formcompiler_system_test(UFLFILE poisson_dg_tensor.ufl
                                  BASENAME sumfact_poisson_dg_tensor
                                  INIFILE poisson_dg_tensor.mini
                                  )

# Slicing vectorization stratgies

dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_poisson_dg_3d_sliced
                                  INIFILE sliced.mini
                                  LABELS quick
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_poisson_dg_3d_diagonal
                                  INIFILE diagonal.mini
                                  )

#======================================
# Test autotuning with google-benchmark
#======================================
if(benchmark_FOUND)
  dune_add_formcompiler_system_test(UFLFILE poisson_3d.ufl
                                    BASENAME sumfact_poisson_3d_benchmark
                                    INIFILE poisson_3d_benchmark.mini
                                    )

  dune_add_formcompiler_system_test(UFLFILE poisson_dg_volumes_3d.ufl
                                    BASENAME sumfact_poisson_fastdg_volumes_3d_benchmark
                                    INIFILE poisson_fastdg_volumes_3d_benchmark.mini
                                    LABELS quick)
endif()


#================================================
# Poisson fastdg with performance transformations
#================================================
dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                  BASENAME sumfact_poisson_fastdg_2d_performance_transformations
                                  INIFILE poisson_fastdg_2d_performance_transformations.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_poisson_fastdg_3d_performance_transformations
                                  INIFILE poisson_fastdg_3d_performance_transformations.mini
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_dg_2d.ufl
                                  BASENAME sumfact_poisson_dg_2d_performance_transformations
                                  INIFILE poisson_dg_2d_performance_transformations.mini
                                  LABELS quick
                                  )
dune_add_formcompiler_system_test(UFLFILE poisson_dg_3d.ufl
                                  BASENAME sumfact_poisson_dg_3d_performance_transformations
                                  INIFILE poisson_dg_3d_performance_transformations.mini
                                  LABELS quick
                                  )
