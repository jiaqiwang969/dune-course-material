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

# Utility rule file for doxyfile.

# Include any custom commands dependencies for this target.
include doc/doxygen/CMakeFiles/doxyfile.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/doxygen/CMakeFiles/doxyfile.dir/progress.make

doc/doxygen/CMakeFiles/doxyfile: doc/doxygen/Doxyfile.in
doc/doxygen/CMakeFiles/doxyfile: doc/doxygen/Doxyfile.in

doc/doxygen/Doxyfile.in: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/Doxystyle
doc/doxygen/Doxyfile.in: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/doxygen-macros
doc/doxygen/Doxyfile.in: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/doc/doxygen/Doxylocal
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --blue --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Creating Doxyfile.in"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc/doxygen && /opt/homebrew/Cellar/cmake/3.20.4/bin/cmake -D DOT_TRUE= -D DUNE_MOD_NAME=dune-testtools -D DUNE_MOD_VERSION=3.0git -D DOXYSTYLE=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/Doxystyle -D DOXYGENMACROS=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/doc/doxygen/doxygen-macros -D DOXYLOCAL=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/doc/doxygen/Doxylocal -D abs_top_srcdir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools -D srcdir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/doc/doxygen -D top_srcdir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools -P /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/cmake/scripts/CreateDoxyFile.cmake

doc/doxygen/Doxyfile: doc/doxygen/Doxyfile.in
	@$(CMAKE_COMMAND) -E touch_nocreate doc/doxygen/Doxyfile

doxyfile: doc/doxygen/CMakeFiles/doxyfile
doxyfile: doc/doxygen/Doxyfile
doxyfile: doc/doxygen/Doxyfile.in
doxyfile: doc/doxygen/CMakeFiles/doxyfile.dir/build.make
.PHONY : doxyfile

# Rule to build all files generated by this target.
doc/doxygen/CMakeFiles/doxyfile.dir/build: doxyfile
.PHONY : doc/doxygen/CMakeFiles/doxyfile.dir/build

doc/doxygen/CMakeFiles/doxyfile.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc/doxygen && $(CMAKE_COMMAND) -P CMakeFiles/doxyfile.dir/cmake_clean.cmake
.PHONY : doc/doxygen/CMakeFiles/doxyfile.dir/clean

doc/doxygen/CMakeFiles/doxyfile.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/doc/doxygen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc/doxygen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/doc/doxygen/CMakeFiles/doxyfile.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/doxygen/CMakeFiles/doxyfile.dir/depend

