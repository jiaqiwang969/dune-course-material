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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions

# Include any dependencies generated for this target.
include dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/flags.make

dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o: dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/flags.make
dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/functionspacebases/test/gridviewfunctionspacebasistest.cc
dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o: dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o -MF CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o.d -o CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/functionspacebases/test/gridviewfunctionspacebasistest.cc

dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/functionspacebases/test/gridviewfunctionspacebasistest.cc > CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.i

dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/functionspacebases/test/gridviewfunctionspacebasistest.cc -o CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.s

# Object files for target gridviewfunctionspacebasistest
gridviewfunctionspacebasistest_OBJECTS = \
"CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o"

# External object files for target gridviewfunctionspacebasistest
gridviewfunctionspacebasistest_EXTERNAL_OBJECTS =

dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/gridviewfunctionspacebasistest.cc.o
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/build.make
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /opt/homebrew/lib/libsuperlu.dylib
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /opt/homebrew/lib/libgmp.dylib
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /opt/homebrew/lib/libgmpxx.dylib
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/functions/functionspacebases/test/gridviewfunctionspacebasistest: dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable gridviewfunctionspacebasistest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/gridviewfunctionspacebasistest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/build: dune/functions/functionspacebases/test/gridviewfunctionspacebasistest
.PHONY : dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/build

dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test && $(CMAKE_COMMAND) -P CMakeFiles/gridviewfunctionspacebasistest.dir/cmake_clean.cmake
.PHONY : dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/clean

dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/functionspacebases/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/functions/functionspacebases/test/CMakeFiles/gridviewfunctionspacebasistest.dir/depend
