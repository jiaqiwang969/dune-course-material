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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools

# Utility rule file for doc_technical_tex_clean.

# Include any custom commands dependencies for this target.
include doc/CMakeFiles/doc_technical_tex_clean.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/CMakeFiles/doc_technical_tex_clean.dir/progress.make

doc/CMakeFiles/doc_technical_tex_clean:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Cleaning build results from target doc_technical_tex"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/doc && /Library/TeX/texbin/latexmk -C -r /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc/doc_technical_tex.latexmkrc technical.tex

doc_technical_tex_clean: doc/CMakeFiles/doc_technical_tex_clean
doc_technical_tex_clean: doc/CMakeFiles/doc_technical_tex_clean.dir/build.make
.PHONY : doc_technical_tex_clean

# Rule to build all files generated by this target.
doc/CMakeFiles/doc_technical_tex_clean.dir/build: doc_technical_tex_clean
.PHONY : doc/CMakeFiles/doc_technical_tex_clean.dir/build

doc/CMakeFiles/doc_technical_tex_clean.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc && $(CMAKE_COMMAND) -P CMakeFiles/doc_technical_tex_clean.dir/cmake_clean.cmake
.PHONY : doc/CMakeFiles/doc_technical_tex_clean.dir/clean

doc/CMakeFiles/doc_technical_tex_clean.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/doc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc/CMakeFiles/doc_technical_tex_clean.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/CMakeFiles/doc_technical_tex_clean.dir/depend

