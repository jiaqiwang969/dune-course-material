# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.20

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:

#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:

# Disable VCS-based implicit rules.
% : %,v

# Disable VCS-based implicit rules.
% : RCS/%

# Disable VCS-based implicit rules.
% : RCS/%,v

# Disable VCS-based implicit rules.
% : SCCS/s.%

# Disable VCS-based implicit rules.
% : s.%

.SUFFIXES: .hpux_make_needs_suffix_list

# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /opt/homebrew/Cellar/cmake/3.20.4/bin/cmake

# The command to remove a file.
RM = /opt/homebrew/Cellar/cmake/3.20.4/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen

# Utility rule file for app_poisson_dg_tensor.

# Include any custom commands dependencies for this target.
include applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/compiler_depend.make

# Include the progress variables for this target.
include applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/progress.make

app_poisson_dg_tensor: applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/build.make
.PHONY : app_poisson_dg_tensor

# Rule to build all files generated by this target.
applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/build: app_poisson_dg_tensor
.PHONY : applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/build

applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/applications/poisson_dg_tensor && $(CMAKE_COMMAND) -P CMakeFiles/app_poisson_dg_tensor.dir/cmake_clean.cmake
.PHONY : applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/clean

applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/applications/poisson_dg_tensor /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/applications/poisson_dg_tensor /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : applications/poisson_dg_tensor/CMakeFiles/app_poisson_dg_tensor.dir/depend

