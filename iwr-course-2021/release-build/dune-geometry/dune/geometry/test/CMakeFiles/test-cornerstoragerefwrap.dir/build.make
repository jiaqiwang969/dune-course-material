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
include dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/progress.make

# Include the compile flags for this target's objects.
include dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/flags.make

dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o: dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/flags.make
dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-cornerstoragerefwrap.cc
dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o: dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o -MF CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o.d -o CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-cornerstoragerefwrap.cc

dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-cornerstoragerefwrap.cc > CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.i

dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test/test-cornerstoragerefwrap.cc -o CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.s

# Object files for target test-cornerstoragerefwrap
test__cornerstoragerefwrap_OBJECTS = \
"CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o"

# External object files for target test-cornerstoragerefwrap
test__cornerstoragerefwrap_EXTERNAL_OBJECTS =

dune/geometry/test/test-cornerstoragerefwrap: dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/test-cornerstoragerefwrap.cc.o
dune/geometry/test/test-cornerstoragerefwrap: dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/build.make
dune/geometry/test/test-cornerstoragerefwrap: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/geometry/test/test-cornerstoragerefwrap: /opt/homebrew/lib/libgmp.dylib
dune/geometry/test/test-cornerstoragerefwrap: /opt/homebrew/lib/libgmpxx.dylib
dune/geometry/test/test-cornerstoragerefwrap: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/geometry/test/test-cornerstoragerefwrap: lib/libdunegeometry.a
dune/geometry/test/test-cornerstoragerefwrap: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/geometry/test/test-cornerstoragerefwrap: dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-cornerstoragerefwrap"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-cornerstoragerefwrap.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/build: dune/geometry/test/test-cornerstoragerefwrap
.PHONY : dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/build

dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test && $(CMAKE_COMMAND) -P CMakeFiles/test-cornerstoragerefwrap.dir/cmake_clean.cmake
.PHONY : dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/clean

dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-geometry/dune/geometry/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/geometry/test/CMakeFiles/test-cornerstoragerefwrap.dir/depend
