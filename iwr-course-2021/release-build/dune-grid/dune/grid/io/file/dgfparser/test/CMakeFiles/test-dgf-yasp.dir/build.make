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
include dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/progress.make

# Include the compile flags for this target's objects.
include dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/flags.make

dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o: dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/flags.make
dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/io/file/dgfparser/test/test-dgf-yasp.cc
dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o: dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o -MF CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o.d -o CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/io/file/dgfparser/test/test-dgf-yasp.cc

dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/io/file/dgfparser/test/test-dgf-yasp.cc > CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.i

dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/io/file/dgfparser/test/test-dgf-yasp.cc -o CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.s

# Object files for target test-dgf-yasp
test__dgf__yasp_OBJECTS = \
"CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o"

# External object files for target test-dgf-yasp
test__dgf__yasp_EXTERNAL_OBJECTS =

dune/grid/io/file/dgfparser/test/test-dgf-yasp: dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/test-dgf-yasp.cc.o
dune/grid/io/file/dgfparser/test/test-dgf-yasp: dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/build.make
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: lib/libdunegrid.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /opt/homebrew/lib/libgmp.dylib
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /opt/homebrew/lib/libgmpxx.dylib
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/grid/io/file/dgfparser/test/test-dgf-yasp: lib/libdunegrid.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/grid/io/file/dgfparser/test/test-dgf-yasp: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/grid/io/file/dgfparser/test/test-dgf-yasp: dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-dgf-yasp"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-dgf-yasp.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/build: dune/grid/io/file/dgfparser/test/test-dgf-yasp
.PHONY : dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/build

dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test && $(CMAKE_COMMAND) -P CMakeFiles/test-dgf-yasp.dir/cmake_clean.cmake
.PHONY : dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/clean

dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-grid/dune/grid/io/file/dgfparser/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/grid/io/file/dgfparser/test/CMakeFiles/test-dgf-yasp.dir/depend

