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
include dune/istl/test/CMakeFiles/multirhstest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/istl/test/CMakeFiles/multirhstest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/istl/test/CMakeFiles/multirhstest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/istl/test/CMakeFiles/multirhstest.dir/flags.make

dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.o: dune/istl/test/CMakeFiles/multirhstest.dir/flags.make
dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multirhstest.cc
dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.o: dune/istl/test/CMakeFiles/multirhstest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.o -MF CMakeFiles/multirhstest.dir/multirhstest.cc.o.d -o CMakeFiles/multirhstest.dir/multirhstest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multirhstest.cc

dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/multirhstest.dir/multirhstest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multirhstest.cc > CMakeFiles/multirhstest.dir/multirhstest.cc.i

dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/multirhstest.dir/multirhstest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multirhstest.cc -o CMakeFiles/multirhstest.dir/multirhstest.cc.s

# Object files for target multirhstest
multirhstest_OBJECTS = \
"CMakeFiles/multirhstest.dir/multirhstest.cc.o"

# External object files for target multirhstest
multirhstest_EXTERNAL_OBJECTS =

dune/istl/test/multirhstest: dune/istl/test/CMakeFiles/multirhstest.dir/multirhstest.cc.o
dune/istl/test/multirhstest: dune/istl/test/CMakeFiles/multirhstest.dir/build.make
dune/istl/test/multirhstest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/istl/test/multirhstest: /opt/homebrew/lib/libsuperlu.dylib
dune/istl/test/multirhstest: /opt/homebrew/lib/libgmp.dylib
dune/istl/test/multirhstest: /opt/homebrew/lib/libgmpxx.dylib
dune/istl/test/multirhstest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/istl/test/multirhstest: dune/istl/test/CMakeFiles/multirhstest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable multirhstest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/multirhstest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/istl/test/CMakeFiles/multirhstest.dir/build: dune/istl/test/multirhstest
.PHONY : dune/istl/test/CMakeFiles/multirhstest.dir/build

dune/istl/test/CMakeFiles/multirhstest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && $(CMAKE_COMMAND) -P CMakeFiles/multirhstest.dir/cmake_clean.cmake
.PHONY : dune/istl/test/CMakeFiles/multirhstest.dir/clean

dune/istl/test/CMakeFiles/multirhstest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test/CMakeFiles/multirhstest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/istl/test/CMakeFiles/multirhstest.dir/depend

