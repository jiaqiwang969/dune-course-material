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
include dune/istl/test/CMakeFiles/superluctest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/istl/test/CMakeFiles/superluctest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/istl/test/CMakeFiles/superluctest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/istl/test/CMakeFiles/superluctest.dir/flags.make

dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.o: dune/istl/test/CMakeFiles/superluctest.dir/flags.make
dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/superlutest.cc
dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.o: dune/istl/test/CMakeFiles/superluctest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.o -MF CMakeFiles/superluctest.dir/superlutest.cc.o.d -o CMakeFiles/superluctest.dir/superlutest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/superlutest.cc

dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/superluctest.dir/superlutest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/superlutest.cc > CMakeFiles/superluctest.dir/superlutest.cc.i

dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/superluctest.dir/superlutest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/superlutest.cc -o CMakeFiles/superluctest.dir/superlutest.cc.s

# Object files for target superluctest
superluctest_OBJECTS = \
"CMakeFiles/superluctest.dir/superlutest.cc.o"

# External object files for target superluctest
superluctest_EXTERNAL_OBJECTS =

dune/istl/test/superluctest: dune/istl/test/CMakeFiles/superluctest.dir/superlutest.cc.o
dune/istl/test/superluctest: dune/istl/test/CMakeFiles/superluctest.dir/build.make
dune/istl/test/superluctest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/istl/test/superluctest: /opt/homebrew/lib/libsuperlu.dylib
dune/istl/test/superluctest: /opt/homebrew/lib/libgmp.dylib
dune/istl/test/superluctest: /opt/homebrew/lib/libgmpxx.dylib
dune/istl/test/superluctest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/istl/test/superluctest: dune/istl/test/CMakeFiles/superluctest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable superluctest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/superluctest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/istl/test/CMakeFiles/superluctest.dir/build: dune/istl/test/superluctest
.PHONY : dune/istl/test/CMakeFiles/superluctest.dir/build

dune/istl/test/CMakeFiles/superluctest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && $(CMAKE_COMMAND) -P CMakeFiles/superluctest.dir/cmake_clean.cmake
.PHONY : dune/istl/test/CMakeFiles/superluctest.dir/clean

dune/istl/test/CMakeFiles/superluctest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test/CMakeFiles/superluctest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/istl/test/CMakeFiles/superluctest.dir/depend

