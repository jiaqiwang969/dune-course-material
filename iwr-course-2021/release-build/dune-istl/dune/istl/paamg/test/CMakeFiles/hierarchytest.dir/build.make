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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl

# Include any dependencies generated for this target.
include dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/flags.make

dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.o: dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/flags.make
dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/paamg/test/hierarchytest.cc
dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.o: dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.o -MF CMakeFiles/hierarchytest.dir/hierarchytest.cc.o.d -o CMakeFiles/hierarchytest.dir/hierarchytest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/paamg/test/hierarchytest.cc

dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/hierarchytest.dir/hierarchytest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/paamg/test/hierarchytest.cc > CMakeFiles/hierarchytest.dir/hierarchytest.cc.i

dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/hierarchytest.dir/hierarchytest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/paamg/test/hierarchytest.cc -o CMakeFiles/hierarchytest.dir/hierarchytest.cc.s

# Object files for target hierarchytest
hierarchytest_OBJECTS = \
"CMakeFiles/hierarchytest.dir/hierarchytest.cc.o"

# External object files for target hierarchytest
hierarchytest_EXTERNAL_OBJECTS =

dune/istl/paamg/test/hierarchytest: dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/hierarchytest.cc.o
dune/istl/paamg/test/hierarchytest: dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/build.make
dune/istl/paamg/test/hierarchytest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/istl/paamg/test/hierarchytest: /opt/homebrew/lib/libsuperlu.dylib
dune/istl/paamg/test/hierarchytest: /opt/homebrew/lib/libgmp.dylib
dune/istl/paamg/test/hierarchytest: /opt/homebrew/lib/libgmpxx.dylib
dune/istl/paamg/test/hierarchytest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/istl/paamg/test/hierarchytest: dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable hierarchytest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/hierarchytest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/build: dune/istl/paamg/test/hierarchytest
.PHONY : dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/build

dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test && $(CMAKE_COMMAND) -P CMakeFiles/hierarchytest.dir/cmake_clean.cmake
.PHONY : dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/clean

dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/paamg/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/istl/paamg/test/CMakeFiles/hierarchytest.dir/depend

