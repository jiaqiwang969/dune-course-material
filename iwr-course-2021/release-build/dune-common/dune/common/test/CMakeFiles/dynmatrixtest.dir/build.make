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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common

# Include any dependencies generated for this target.
include dune/common/test/CMakeFiles/dynmatrixtest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/common/test/CMakeFiles/dynmatrixtest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/common/test/CMakeFiles/dynmatrixtest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/common/test/CMakeFiles/dynmatrixtest.dir/flags.make

dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o: dune/common/test/CMakeFiles/dynmatrixtest.dir/flags.make
dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/dune/common/test/dynmatrixtest.cc
dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o: dune/common/test/CMakeFiles/dynmatrixtest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o -MF CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o.d -o CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/dune/common/test/dynmatrixtest.cc

dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/dune/common/test/dynmatrixtest.cc > CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.i

dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/dune/common/test/dynmatrixtest.cc -o CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.s

# Object files for target dynmatrixtest
dynmatrixtest_OBJECTS = \
"CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o"

# External object files for target dynmatrixtest
dynmatrixtest_EXTERNAL_OBJECTS =

dune/common/test/dynmatrixtest: dune/common/test/CMakeFiles/dynmatrixtest.dir/dynmatrixtest.cc.o
dune/common/test/dynmatrixtest: dune/common/test/CMakeFiles/dynmatrixtest.dir/build.make
dune/common/test/dynmatrixtest: /opt/homebrew/lib/libgmp.dylib
dune/common/test/dynmatrixtest: /opt/homebrew/lib/libgmpxx.dylib
dune/common/test/dynmatrixtest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/common/test/dynmatrixtest: lib/libdunecommon.a
dune/common/test/dynmatrixtest: dune/common/test/CMakeFiles/dynmatrixtest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable dynmatrixtest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/dynmatrixtest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/common/test/CMakeFiles/dynmatrixtest.dir/build: dune/common/test/dynmatrixtest
.PHONY : dune/common/test/CMakeFiles/dynmatrixtest.dir/build

dune/common/test/CMakeFiles/dynmatrixtest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test && $(CMAKE_COMMAND) -P CMakeFiles/dynmatrixtest.dir/cmake_clean.cmake
.PHONY : dune/common/test/CMakeFiles/dynmatrixtest.dir/clean

dune/common/test/CMakeFiles/dynmatrixtest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/dune/common/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/test/CMakeFiles/dynmatrixtest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/common/test/CMakeFiles/dynmatrixtest.dir/depend

