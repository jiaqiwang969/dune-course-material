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

# Utility rule file for sumfact_poisson_2d.

# Include any custom commands dependencies for this target.
include test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/compiler_depend.make

# Include the progress variables for this target.
include test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/progress.make

sumfact_poisson_2d: test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/build.make
.PHONY : sumfact_poisson_2d

# Rule to build all files generated by this target.
test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/build: sumfact_poisson_2d
.PHONY : test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/build

test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/poisson && $(CMAKE_COMMAND) -P CMakeFiles/sumfact_poisson_2d.dir/cmake_clean.cmake
.PHONY : test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/clean

test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/sumfact/poisson /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/poisson /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/sumfact/poisson/CMakeFiles/sumfact_poisson_2d.dir/depend

