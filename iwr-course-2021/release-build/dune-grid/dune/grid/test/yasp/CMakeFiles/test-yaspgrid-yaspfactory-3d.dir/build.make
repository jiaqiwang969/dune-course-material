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
include dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/progress.make

# Include the compile flags for this target's objects.
include dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/flags.make

dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o: dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/flags.make
dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d.cc
dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o: dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o -MF CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o.d -o CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d.cc

dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d.cc > CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.i

dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d.cc -o CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.s

# Object files for target test-yaspgrid-yaspfactory-3d
test__yaspgrid__yaspfactory__3d_OBJECTS = \
"CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o"

# External object files for target test-yaspgrid-yaspfactory-3d
test__yaspgrid__yaspfactory__3d_EXTERNAL_OBJECTS =

dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/test-yaspgrid-yaspfactory-3d.cc.o
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/build.make
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: lib/libdunegrid.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /opt/homebrew/lib/libgmp.dylib
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /opt/homebrew/lib/libgmpxx.dylib
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d: dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-yaspgrid-yaspfactory-3d"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/build: dune/grid/test/yasp/test-yaspgrid-yaspfactory-3d
.PHONY : dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/build

dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp && $(CMAKE_COMMAND) -P CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/cmake_clean.cmake
.PHONY : dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/clean

dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/test/yasp /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/grid/test/yasp/CMakeFiles/test-yaspgrid-yaspfactory-3d.dir/depend
