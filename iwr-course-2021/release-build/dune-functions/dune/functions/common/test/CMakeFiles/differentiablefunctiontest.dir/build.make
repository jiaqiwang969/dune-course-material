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
include dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/flags.make

dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o: dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/flags.make
dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/common/test/differentiablefunctiontest.cc
dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o: dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o -MF CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o.d -o CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/common/test/differentiablefunctiontest.cc

dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/common/test/differentiablefunctiontest.cc > CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.i

dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/common/test/differentiablefunctiontest.cc -o CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.s

# Object files for target differentiablefunctiontest
differentiablefunctiontest_OBJECTS = \
"CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o"

# External object files for target differentiablefunctiontest
differentiablefunctiontest_EXTERNAL_OBJECTS =

dune/functions/common/test/differentiablefunctiontest: dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/differentiablefunctiontest.cc.o
dune/functions/common/test/differentiablefunctiontest: dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/build.make
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/functions/common/test/differentiablefunctiontest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/functions/common/test/differentiablefunctiontest: /opt/homebrew/lib/libsuperlu.dylib
dune/functions/common/test/differentiablefunctiontest: /opt/homebrew/lib/libgmp.dylib
dune/functions/common/test/differentiablefunctiontest: /opt/homebrew/lib/libgmpxx.dylib
dune/functions/common/test/differentiablefunctiontest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/functions/common/test/differentiablefunctiontest: dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable differentiablefunctiontest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/differentiablefunctiontest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/build: dune/functions/common/test/differentiablefunctiontest
.PHONY : dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/build

dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test && $(CMAKE_COMMAND) -P CMakeFiles/differentiablefunctiontest.dir/cmake_clean.cmake
.PHONY : dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/clean

dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/dune/functions/common/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/functions/common/test/CMakeFiles/differentiablefunctiontest.dir/depend

