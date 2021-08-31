if(consistent-edge-orientation_FOUND)
  dune_add_formcompiler_system_test(UFLFILE poisson_dg_only_skeletons_3d.ufl
                                    BASENAME sumfact_poisson_dg_3d_facedir_facemod_variation
                                    INIFILE sumfact_poisson_dg_3d_facedir_facemod_variation.mini
                                    SOURCE sumfact_poisson_dg_3d_facedir_facemod_variation_driver.cc
                                    ANALYZE_GRID
                                    )

  dune_add_formcompiler_system_test(UFLFILE poisson_dg_only_skeletons_3d.ufl
                                    BASENAME sumfact_poisson_fastdg_3d_facedir_facemod_variation
                                    INIFILE sumfact_poisson_fastdg_3d_facedir_facemod_variation.mini
                                    SOURCE sumfact_poisson_fastdg_3d_facedir_facemod_variation_driver.cc
                                    ANALYZE_GRID
                                    )


  # This can be used to verify the results from the actual test. Make sure to
  # adjust the gmsh file in the ini file!

  # dune_add_formcompiler_system_test(UFLFILE poisson_dg_only_skeletons_3d.ufl
  #                                   BASENAME poisson_dg_3d_facedir_facemod_variation
  #                                   INIFILE poisson_dg_3d_facedir_facemod_variation.mini
  #                                   SOURCE poisson_dg_3d_facedir_facemod_variation_driver.cc
  #                                   ANALYZE_GRID
  #                                   )


  dune_symlink_to_source_files(FILES grid_unstructured_00.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_01.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_02.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_03.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_04.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_05.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_06.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_07.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_08.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_09.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_10.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_11.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_12.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_13.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_14.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_15.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_16.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_17.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_18.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_19.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_20.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_21.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_22.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_23.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_24.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_25.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_26.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_27.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_28.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_29.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_30.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_31.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_32.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_33.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_34.msh)
  dune_symlink_to_source_files(FILES grid_unstructured_35.msh)
endif()
