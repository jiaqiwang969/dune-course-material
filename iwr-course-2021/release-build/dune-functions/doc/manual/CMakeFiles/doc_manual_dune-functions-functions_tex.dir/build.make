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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions

# Utility rule file for doc_manual_dune-functions-functions_tex.

# Include any custom commands dependencies for this target.
include doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/progress.make

doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building PDF from dune-functions-functions.tex..."
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/doc/manual && /Library/TeX/texbin/latexmk -r /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/doc/manual/doc_manual_dune-functions-functions_tex.latexmkrc dune-functions-functions.tex

doc_manual_dune-functions-functions_tex: doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex
doc_manual_dune-functions-functions_tex: doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/build.make
.PHONY : doc_manual_dune-functions-functions_tex

# Rule to build all files generated by this target.
doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/build: doc_manual_dune-functions-functions_tex
.PHONY : doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/build

doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/doc/manual && $(CMAKE_COMMAND) -P CMakeFiles/doc_manual_dune-functions-functions_tex.dir/cmake_clean.cmake
.PHONY : doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/clean

doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/doc/manual /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/doc/manual /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/manual/CMakeFiles/doc_manual_dune-functions-functions_tex.dir/depend

