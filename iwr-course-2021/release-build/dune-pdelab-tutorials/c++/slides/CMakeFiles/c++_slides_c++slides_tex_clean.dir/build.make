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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials

# Utility rule file for c++_slides_c++slides_tex_clean.

# Include any custom commands dependencies for this target.
include c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/compiler_depend.make

# Include the progress variables for this target.
include c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/progress.make

c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean:
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Cleaning build results from target c++_slides_c++slides_tex"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/slides && /opt/homebrew/Cellar/cmake/3.20.4/bin/cmake -E env openout_any="a" /Library/TeX/texbin/latexmk -C -r /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/slides/c++_slides_c++slides_tex.latexmkrc /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/slides/c++_slides_c++slides_tex_source.cc

c++_slides_c++slides_tex_clean: c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean
c++_slides_c++slides_tex_clean: c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/build.make
.PHONY : c++_slides_c++slides_tex_clean

# Rule to build all files generated by this target.
c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/build: c++_slides_c++slides_tex_clean
.PHONY : c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/build

c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/slides && $(CMAKE_COMMAND) -P CMakeFiles/c++_slides_c++slides_tex_clean.dir/cmake_clean.cmake
.PHONY : c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/clean

c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/slides /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/slides /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : c++/slides/CMakeFiles/c++_slides_c++slides_tex_clean.dir/depend
