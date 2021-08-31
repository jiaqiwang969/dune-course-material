add_subdirectory(blockstructured)
add_subdirectory(common)
add_subdirectory(sumfact)
add_subdirectory(test)

install(FILES vectorclass/instrset.h
              vectorclass/vector_convert.h
              vectorclass/vectorclass.h
              vectorclass/vectorf128.h
              vectorclass/vectorf256e.h
              vectorclass/vectorf256.h
              vectorclass/vectorf512e.h
              vectorclass/vectorf512.h
              vectorclass/vectori128.h
              vectorclass/vectori256e.h
              vectorclass/vectori256.h
              vectorclass/vectori512e.h
              vectorclass/vectori512.h
              vectorclass/vectori512s.h
              vectorclass/vectori512se.h
              vectorclass/vectormath_common.h
              vectorclass/vectormath_exp.h
              vectorclass/vectormath_hyp.h
              vectorclass/vectormath_lib.h
              vectorclass/vectormath_trig.h
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen/vectorclass)

install(FILES localbasiscache.hh
              matrixfree.hh
              matrixfreeistlbackends.hh
              matrixfreenewton.hh
              newtonbase.hh
              vtkpredicate.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen
        )
