dune_add_formcompiler_system_test(UFLFILE poisson.ufl
                                  SOURCE coeffeval_poisson.cc
                                  INIFILE coeffeval_poisson.mini
                                  BASENAME coeffeval_poisson
                                  LABELS quick)
