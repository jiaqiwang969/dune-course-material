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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree

# Include any dependencies generated for this target.
include test/CMakeFiles/testtreecontainer.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/CMakeFiles/testtreecontainer.dir/compiler_depend.make

# Include the progress variables for this target.
include test/CMakeFiles/testtreecontainer.dir/progress.make

# Include the compile flags for this target's objects.
include test/CMakeFiles/testtreecontainer.dir/flags.make

test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o: test/CMakeFiles/testtreecontainer.dir/flags.make
test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree/test/testtreecontainer.cc
test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o: test/CMakeFiles/testtreecontainer.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o -MF CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o.d -o CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree/test/testtreecontainer.cc

test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree/test/testtreecontainer.cc > CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.i

test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree/test/testtreecontainer.cc -o CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.s

# Object files for target testtreecontainer
testtreecontainer_OBJECTS = \
"CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o"

# External object files for target testtreecontainer
testtreecontainer_EXTERNAL_OBJECTS =

test/testtreecontainer: test/CMakeFiles/testtreecontainer.dir/testtreecontainer.cc.o
test/testtreecontainer: test/CMakeFiles/testtreecontainer.dir/build.make
test/testtreecontainer: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
test/testtreecontainer: /opt/homebrew/lib/libgmp.dylib
test/testtreecontainer: /opt/homebrew/lib/libgmpxx.dylib
test/testtreecontainer: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
test/testtreecontainer: test/CMakeFiles/testtreecontainer.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable testtreecontainer"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/testtreecontainer.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/CMakeFiles/testtreecontainer.dir/build: test/testtreecontainer
.PHONY : test/CMakeFiles/testtreecontainer.dir/build

test/CMakeFiles/testtreecontainer.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test && $(CMAKE_COMMAND) -P CMakeFiles/testtreecontainer.dir/cmake_clean.cmake
.PHONY : test/CMakeFiles/testtreecontainer.dir/clean

test/CMakeFiles/testtreecontainer.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-typetree/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-typetree/test/CMakeFiles/testtreecontainer.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/CMakeFiles/testtreecontainer.dir/depend

