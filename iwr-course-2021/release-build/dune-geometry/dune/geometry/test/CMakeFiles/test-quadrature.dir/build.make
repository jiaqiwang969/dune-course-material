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

# Include any dependencies generated for this target.
include dune/geometry/test/CMakeFiles/test-quadrature.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/geometry/test/CMakeFiles/test-quadrature.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/geometry/test/CMakeFiles/test-quadrature.dir/progress.make

# Include the compile flags for this target's objects.
include dune/geometry/test/CMakeFiles/test-quadrature.dir/flags.make

dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.o: dune/geometry/test/CMakeFiles/test-quadrature.dir/flags.make
dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-quadrature.cc
dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.o: dune/geometry/test/CMakeFiles/test-quadrature.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.o -MF CMakeFiles/test-quadrature.dir/test-quadrature.cc.o.d -o CMakeFiles/test-quadrature.dir/test-quadrature.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-quadrature.cc

dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-quadrature.dir/test-quadrature.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-quadrature.cc > CMakeFiles/test-quadrature.dir/test-quadrature.cc.i

dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-quadrature.dir/test-quadrature.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-quadrature.cc -o CMakeFiles/test-quadrature.dir/test-quadrature.cc.s

# Object files for target test-quadrature
test__quadrature_OBJECTS = \
"CMakeFiles/test-quadrature.dir/test-quadrature.cc.o"

# External object files for target test-quadrature
test__quadrature_EXTERNAL_OBJECTS =

dune/geometry/test/test-quadrature: dune/geometry/test/CMakeFiles/test-quadrature.dir/test-quadrature.cc.o
dune/geometry/test/test-quadrature: dune/geometry/test/CMakeFiles/test-quadrature.dir/build.make
dune/geometry/test/test-quadrature: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/geometry/test/test-quadrature: /opt/homebrew/lib/libgmp.dylib
dune/geometry/test/test-quadrature: /opt/homebrew/lib/libgmpxx.dylib
dune/geometry/test/test-quadrature: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/geometry/test/test-quadrature: lib/libdunegeometry.a
dune/geometry/test/test-quadrature: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/geometry/test/test-quadrature: dune/geometry/test/CMakeFiles/test-quadrature.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-quadrature"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-quadrature.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/geometry/test/CMakeFiles/test-quadrature.dir/build: dune/geometry/test/test-quadrature
.PHONY : dune/geometry/test/CMakeFiles/test-quadrature.dir/build

dune/geometry/test/CMakeFiles/test-quadrature.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && $(CMAKE_COMMAND) -P CMakeFiles/test-quadrature.dir/cmake_clean.cmake
.PHONY : dune/geometry/test/CMakeFiles/test-quadrature.dir/clean

dune/geometry/test/CMakeFiles/test-quadrature.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test/CMakeFiles/test-quadrature.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/geometry/test/CMakeFiles/test-quadrature.dir/depend

