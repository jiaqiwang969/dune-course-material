dune_python_install_package(PATH .)

dune_symlink_to_source_files(FILES make_graph.sh
                                   knltimings.sh
                                   )

add_subdirectory(analyzegrid)
