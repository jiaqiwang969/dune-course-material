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
include dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/flags.make

dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o: dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/flags.make
dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multitypeblockvectortest.cc
dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o: dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o -MF CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o.d -o CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multitypeblockvectortest.cc

dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multitypeblockvectortest.cc > CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.i

dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test/multitypeblockvectortest.cc -o CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.s

# Object files for target multitypeblockvectortest
multitypeblockvectortest_OBJECTS = \
"CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o"

# External object files for target multitypeblockvectortest
multitypeblockvectortest_EXTERNAL_OBJECTS =

dune/istl/test/multitypeblockvectortest: dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/multitypeblockvectortest.cc.o
dune/istl/test/multitypeblockvectortest: dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/build.make
dune/istl/test/multitypeblockvectortest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/istl/test/multitypeblockvectortest: /opt/homebrew/lib/libsuperlu.dylib
dune/istl/test/multitypeblockvectortest: /opt/homebrew/lib/libgmp.dylib
dune/istl/test/multitypeblockvectortest: /opt/homebrew/lib/libgmpxx.dylib
dune/istl/test/multitypeblockvectortest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/istl/test/multitypeblockvectortest: dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable multitypeblockvectortest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/multitypeblockvectortest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/build: dune/istl/test/multitypeblockvectortest
.PHONY : dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/build

dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test && $(CMAKE_COMMAND) -P CMakeFiles/multitypeblockvectortest.dir/cmake_clean.cmake
.PHONY : dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/clean

dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-istl/dune/istl/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-istl/dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/istl/test/CMakeFiles/multitypeblockvectortest.dir/depend

