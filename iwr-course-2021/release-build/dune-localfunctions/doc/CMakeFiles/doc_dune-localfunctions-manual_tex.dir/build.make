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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions

# Utility rule file for doc_dune-localfunctions-manual_tex.

# Include any custom commands dependencies for this target.
include doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/progress.make

doc/CMakeFiles/doc_dune-localfunctions-manual_tex:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building PDF from dune-localfunctions-manual.tex..."
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/doc && /Library/TeX/texbin/latexmk -r /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/doc/doc_dune-localfunctions-manual_tex.latexmkrc dune-localfunctions-manual.tex

doc_dune-localfunctions-manual_tex: doc/CMakeFiles/doc_dune-localfunctions-manual_tex
doc_dune-localfunctions-manual_tex: doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/build.make
.PHONY : doc_dune-localfunctions-manual_tex

# Rule to build all files generated by this target.
doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/build: doc_dune-localfunctions-manual_tex
.PHONY : doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/build

doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/doc && $(CMAKE_COMMAND) -P CMakeFiles/doc_dune-localfunctions-manual_tex.dir/cmake_clean.cmake
.PHONY : doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/clean

doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/doc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/doc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/CMakeFiles/doc_dune-localfunctions-manual_tex.dir/depend

