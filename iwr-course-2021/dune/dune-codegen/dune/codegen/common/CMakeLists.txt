set(CMAKE_MACOSX_RPATH 1)
install(FILES muladd_workarounds.hh
              simdtraits.hh
              timer.hh
              timer_tsc.hh
              timer_chrono.hh
              tsc.hh
              vcltraits.hh
              vectorclass.hh
        DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/dune/codegen/common
        )
