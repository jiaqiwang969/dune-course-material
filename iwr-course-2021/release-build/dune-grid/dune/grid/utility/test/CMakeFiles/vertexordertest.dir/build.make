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
include dune/grid/utility/test/CMakeFiles/vertexordertest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/grid/utility/test/CMakeFiles/vertexordertest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/grid/utility/test/CMakeFiles/vertexordertest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/grid/utility/test/CMakeFiles/vertexordertest.dir/flags.make

dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.o: dune/grid/utility/test/CMakeFiles/vertexordertest.dir/flags.make
dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/utility/test/vertexordertest.cc
dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.o: dune/grid/utility/test/CMakeFiles/vertexordertest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.o -MF CMakeFiles/vertexordertest.dir/vertexordertest.cc.o.d -o CMakeFiles/vertexordertest.dir/vertexordertest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/utility/test/vertexordertest.cc

dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/vertexordertest.dir/vertexordertest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/utility/test/vertexordertest.cc > CMakeFiles/vertexordertest.dir/vertexordertest.cc.i

dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/vertexordertest.dir/vertexordertest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/utility/test/vertexordertest.cc -o CMakeFiles/vertexordertest.dir/vertexordertest.cc.s

# Object files for target vertexordertest
vertexordertest_OBJECTS = \
"CMakeFiles/vertexordertest.dir/vertexordertest.cc.o"

# External object files for target vertexordertest
vertexordertest_EXTERNAL_OBJECTS =

dune/grid/utility/test/vertexordertest: dune/grid/utility/test/CMakeFiles/vertexordertest.dir/vertexordertest.cc.o
dune/grid/utility/test/vertexordertest: dune/grid/utility/test/CMakeFiles/vertexordertest.dir/build.make
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/utility/test/vertexordertest: lib/libdunegrid.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/utility/test/vertexordertest: /opt/homebrew/lib/libgmp.dylib
dune/grid/utility/test/vertexordertest: /opt/homebrew/lib/libgmpxx.dylib
dune/grid/utility/test/vertexordertest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/grid/utility/test/vertexordertest: lib/libdunegrid.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/utility/test/vertexordertest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/utility/test/vertexordertest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/grid/utility/test/vertexordertest: dune/grid/utility/test/CMakeFiles/vertexordertest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable vertexordertest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/vertexordertest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/grid/utility/test/CMakeFiles/vertexordertest.dir/build: dune/grid/utility/test/vertexordertest
.PHONY : dune/grid/utility/test/CMakeFiles/vertexordertest.dir/build

dune/grid/utility/test/CMakeFiles/vertexordertest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test && $(CMAKE_COMMAND) -P CMakeFiles/vertexordertest.dir/cmake_clean.cmake
.PHONY : dune/grid/utility/test/CMakeFiles/vertexordertest.dir/clean

dune/grid/utility/test/CMakeFiles/vertexordertest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/utility/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/utility/test/CMakeFiles/vertexordertest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/grid/utility/test/CMakeFiles/vertexordertest.dir/depend

