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

# Utility rule file for heatequation.

# Include any custom commands dependencies for this target.
include test/heatequation/CMakeFiles/heatequation.dir/compiler_depend.make

# Include the progress variables for this target.
include test/heatequation/CMakeFiles/heatequation.dir/progress.make

heatequation: test/heatequation/CMakeFiles/heatequation.dir/build.make
.PHONY : heatequation

# Rule to build all files generated by this target.
test/heatequation/CMakeFiles/heatequation.dir/build: heatequation
.PHONY : test/heatequation/CMakeFiles/heatequation.dir/build

test/heatequation/CMakeFiles/heatequation.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/heatequation && $(CMAKE_COMMAND) -P CMakeFiles/heatequation.dir/cmake_clean.cmake
.PHONY : test/heatequation/CMakeFiles/heatequation.dir/clean

test/heatequation/CMakeFiles/heatequation.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/heatequation /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/heatequation /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/heatequation/CMakeFiles/heatequation.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/heatequation/CMakeFiles/heatequation.dir/depend
