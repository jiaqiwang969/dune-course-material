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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl

# Utility rule file for doc_istl_tex.

# Include any custom commands dependencies for this target.
include doc/CMakeFiles/doc_istl_tex.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/CMakeFiles/doc_istl_tex.dir/progress.make

doc/CMakeFiles/doc_istl_tex:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building PDF from istl.tex..."
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/doc && /Library/TeX/texbin/latexmk -r /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/doc/doc_istl_tex.latexmkrc istl.tex

doc_istl_tex: doc/CMakeFiles/doc_istl_tex
doc_istl_tex: doc/CMakeFiles/doc_istl_tex.dir/build.make
.PHONY : doc_istl_tex

# Rule to build all files generated by this target.
doc/CMakeFiles/doc_istl_tex.dir/build: doc_istl_tex
.PHONY : doc/CMakeFiles/doc_istl_tex.dir/build

doc/CMakeFiles/doc_istl_tex.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/doc && $(CMAKE_COMMAND) -P CMakeFiles/doc_istl_tex.dir/cmake_clean.cmake
.PHONY : doc/CMakeFiles/doc_istl_tex.dir/clean

doc/CMakeFiles/doc_istl_tex.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/doc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/doc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/doc/CMakeFiles/doc_istl_tex.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/CMakeFiles/doc_istl_tex.dir/depend

