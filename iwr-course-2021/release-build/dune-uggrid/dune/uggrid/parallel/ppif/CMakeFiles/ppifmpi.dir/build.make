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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid

# Include any dependencies generated for this target.
include dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/flags.make

dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o: dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/flags.make
dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppif.cc
dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o: dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o -MF CMakeFiles/ppifmpi.dir/ppif.cc.o.d -o CMakeFiles/ppifmpi.dir/ppif.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppif.cc

dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ppifmpi.dir/ppif.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppif.cc > CMakeFiles/ppifmpi.dir/ppif.cc.i

dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ppifmpi.dir/ppif.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppif.cc -o CMakeFiles/ppifmpi.dir/ppif.cc.s

ppifmpi: dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o
ppifmpi: dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/build.make
.PHONY : ppifmpi

# Rule to build all files generated by this target.
dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/build: ppifmpi
.PHONY : dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/build

dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif && $(CMAKE_COMMAND) -P CMakeFiles/ppifmpi.dir/cmake_clean.cmake
.PHONY : dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/clean

dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/depend

