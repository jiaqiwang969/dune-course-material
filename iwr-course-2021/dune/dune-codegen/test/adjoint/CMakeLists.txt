dune_add_formcompiler_system_test(UFLFILE poisson_mc.ufl
  BASENAME adjoint_poisson_mc
  INIFILE poisson_mc.ini
  SOURCE poisson_mc_main.cc
  LABELS quick)
