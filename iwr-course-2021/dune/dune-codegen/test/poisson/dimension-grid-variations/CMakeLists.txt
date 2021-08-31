#================
# 1D Tests: cg/dg
#================

dune_add_formcompiler_system_test(UFLFILE poisson_1d_cg_interval.ufl
                                  BASENAME poisson_1d_cg_interval
                                  INIFILE poisson_1d_cg_interval.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_1d_dg_interval.ufl
                                  BASENAME poisson_1d_dg_interval
                                  INIFILE poisson_1d_dg_interval.mini
                                  )

#========================================
# 2D Tests: cg/dg, triangle/quadrilateral
#========================================

dune_add_formcompiler_system_test(UFLFILE poisson_2d_cg_triangle.ufl
                                  BASENAME poisson_2d_cg_triangle
                                  INIFILE poisson_2d_cg_triangle.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_2d_dg_triangle.ufl
                                  BASENAME poisson_2d_dg_triangle
                                  INIFILE poisson_2d_dg_triangle.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_2d_cg_quadrilateral.ufl
                                  BASENAME poisson_2d_cg_quadrilateral
                                  INIFILE poisson_2d_cg_quadrilateral.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_2d_dg_quadrilateral.ufl
                                  BASENAME poisson_2d_dg_quadrilateral
                                  INIFILE poisson_2d_dg_quadrilateral.mini
                                  )

#========================================
# 3D Tests: cg/dg, tetrahedron/hexahedron
#========================================

dune_add_formcompiler_system_test(UFLFILE poisson_3d_cg_tetrahedron.ufl
                                  BASENAME poisson_3d_cg_tetrahedron
                                  INIFILE poisson_3d_cg_tetrahedron.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_3d_dg_tetrahedron.ufl
                                  BASENAME poisson_3d_dg_tetrahedron
                                  INIFILE poisson_3d_dg_tetrahedron.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_3d_cg_hexahedron.ufl
                                  BASENAME poisson_3d_cg_hexahedron
                                  INIFILE poisson_3d_cg_hexahedron.mini
                                  )

dune_add_formcompiler_system_test(UFLFILE poisson_3d_dg_hexahedron.ufl
                                  BASENAME poisson_3d_dg_hexahedron
                                  INIFILE poisson_3d_dg_hexahedron.mini
                                  )
