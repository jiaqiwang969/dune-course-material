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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry

# Utility rule file for doxygen_dune-geometry.

# Include any custom commands dependencies for this target.
include doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/progress.make

doc/doxygen/CMakeFiles/doxygen_dune-geometry: doc/doxygen/html

doc/doxygen/html: doc/doxygen/Doxyfile.in
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building doxygen documentation. This may take a while"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/doc/doxygen && /opt/homebrew/Cellar/cmake/3.20.4/bin/cmake -D DOXYGEN_EXECUTABLE=/opt/homebrew/bin/doxygen -P /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/scripts/RunDoxygen.cmake

doc/doxygen/Doxyfile.in: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/Doxystyle
doc/doxygen/Doxyfile.in: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/doxygen-macros
doc/doxygen/Doxyfile.in: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/doc/doxygen/Doxylocal
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Creating Doxyfile.in"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/doc/doxygen && /opt/homebrew/Cellar/cmake/3.20.4/bin/cmake -D DOT_TRUE= -D DUNE_MOD_NAME=dune-geometry -D DUNE_MOD_VERSION=2.7.1 -D DOXYSTYLE=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/Doxystyle -D DOXYGENMACROS=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/doxygen-macros -D DOXYLOCAL=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/doc/doxygen/Doxylocal -D abs_top_srcdir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry -D srcdir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/doc/doxygen -D top_srcdir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry -P /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/scripts/CreateDoxyFile.cmake

doc/doxygen/Doxyfile: doc/doxygen/Doxyfile.in
	@$(CMAKE_COMMAND) -E touch_nocreate doc/doxygen/Doxyfile

doxygen_dune-geometry: doc/doxygen/CMakeFiles/doxygen_dune-geometry
doxygen_dune-geometry: doc/doxygen/Doxyfile
doxygen_dune-geometry: doc/doxygen/Doxyfile.in
doxygen_dune-geometry: doc/doxygen/html
doxygen_dune-geometry: doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/build.make
.PHONY : doxygen_dune-geometry

# Rule to build all files generated by this target.
doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/build: doxygen_dune-geometry
.PHONY : doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/build

doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/doc/doxygen && $(CMAKE_COMMAND) -P CMakeFiles/doxygen_dune-geometry.dir/cmake_clean.cmake
.PHONY : doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/clean

doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/doc/doxygen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/doc/doxygen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/doxygen/CMakeFiles/doxygen_dune-geometry.dir/depend

