add_executable(taylor-green taylor-green.cc)
dune_symlink_to_source_files(FILES taylor-green.ini)
set_target_properties(taylor-green PROPERTIES EXCLUDE_FROM_ALL 1)
