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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab

# Include any dependencies generated for this target.
include dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/progress.make

# Include the compile flags for this target's objects.
include dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/flags.make

dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o: dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/flags.make
dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testpoisson-periodic-2d.cc
dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o: dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o -MF CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o.d -o CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testpoisson-periodic-2d.cc

dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testpoisson-periodic-2d.cc > CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.i

dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testpoisson-periodic-2d.cc -o CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.s

# Object files for target testpoisson-periodic-2d-deg1-dg1-parallel
testpoisson__periodic__2d__deg1__dg1__parallel_OBJECTS = \
"CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o"

# External object files for target testpoisson-periodic-2d-deg1-dg1-parallel
testpoisson__periodic__2d__deg1__dg1__parallel_EXTERNAL_OBJECTS =

dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/testpoisson-periodic-2d.cc.o
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/build.make
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/lib/libsuperlu.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/lib/libgmp.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/lib/libgmpxx.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: lib/libdunepdelab.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/lib/libsuperlu.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/lib/libgmp.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/lib/libgmpxx.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel: dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable testpoisson-periodic-2d-deg1-dg1-parallel"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/build: dune/pdelab/test/testpoisson-periodic-2d-deg1-dg1-parallel
.PHONY : dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/build

dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && $(CMAKE_COMMAND) -P CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/cmake_clean.cmake
.PHONY : dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/clean

dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/pdelab/test/CMakeFiles/testpoisson-periodic-2d-deg1-dg1-parallel.dir/depend

