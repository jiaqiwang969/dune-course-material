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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid

# Include any dependencies generated for this target.
include dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/progress.make

# Include the compile flags for this target's objects.
include dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/flags.make

dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o: dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/flags.make
dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/test-hierarchicsearch.cc
dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o: dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o -MF CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o.d -o CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/test-hierarchicsearch.cc

dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/test-hierarchicsearch.cc > CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.i

dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/test-hierarchicsearch.cc -o CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.s

# Object files for target test-hierarchicsearch
test__hierarchicsearch_OBJECTS = \
"CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o"

# External object files for target test-hierarchicsearch
test__hierarchicsearch_EXTERNAL_OBJECTS =

dune/grid/test/test-hierarchicsearch: dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/test-hierarchicsearch.cc.o
dune/grid/test/test-hierarchicsearch: dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/build.make
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/test/test-hierarchicsearch: lib/libdunegrid.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/test/test-hierarchicsearch: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/test/test-hierarchicsearch: /opt/homebrew/lib/libgmp.dylib
dune/grid/test/test-hierarchicsearch: /opt/homebrew/lib/libgmpxx.dylib
dune/grid/test/test-hierarchicsearch: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/grid/test/test-hierarchicsearch: dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-hierarchicsearch"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-hierarchicsearch.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/build: dune/grid/test/test-hierarchicsearch
.PHONY : dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/build

dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test && $(CMAKE_COMMAND) -P CMakeFiles/test-hierarchicsearch.dir/cmake_clean.cmake
.PHONY : dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/clean

dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/grid/test/CMakeFiles/test-hierarchicsearch.dir/depend

