if(consistent-edge-orientation_FOUND)
  add_executable(analyze_grid analyze_grid.cc)
  dune_symlink_to_source_files(FILES test_2d_structured.ini test_3d_structured.ini test_2d_unstructured.ini test_3d_unstructured.ini)

  add_executable(consistent_gmsh consistent_gmsh.cc)
endif()
