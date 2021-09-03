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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen

# Include any dependencies generated for this target.
include test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/compiler_depend.make

# Include the progress variables for this target.
include test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/progress.make

# Include the compile flags for this target's objects.
include test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/flags.make

test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.o: test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/flags.make
test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/navier-stokes/reference_program/taylor-green.cc
test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.o: test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.o -MF CMakeFiles/taylor-green.dir/taylor-green.cc.o.d -o CMakeFiles/taylor-green.dir/taylor-green.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/navier-stokes/reference_program/taylor-green.cc

test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/taylor-green.dir/taylor-green.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/navier-stokes/reference_program/taylor-green.cc > CMakeFiles/taylor-green.dir/taylor-green.cc.i

test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/taylor-green.dir/taylor-green.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/navier-stokes/reference_program/taylor-green.cc -o CMakeFiles/taylor-green.dir/taylor-green.cc.s

# Object files for target taylor-green
taylor__green_OBJECTS = \
"CMakeFiles/taylor-green.dir/taylor-green.cc.o"

# External object files for target taylor-green
taylor__green_EXTERNAL_OBJECTS =

test/navier-stokes/reference_program/taylor-green: test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/taylor-green.cc.o
test/navier-stokes/reference_program/taylor-green: test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/build.make
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/lib/libdunepdelab.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
test/navier-stokes/reference_program/taylor-green: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/lib/libsuperlu.dylib
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/lib/libgmp.dylib
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/lib/libgmpxx.dylib
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
test/navier-stokes/reference_program/taylor-green: lib/libdunecodegen.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/lib/libdunepdelab.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
test/navier-stokes/reference_program/taylor-green: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
test/navier-stokes/reference_program/taylor-green: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/lib/libsuperlu.dylib
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/lib/libgmp.dylib
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/lib/libgmpxx.dylib
test/navier-stokes/reference_program/taylor-green: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
test/navier-stokes/reference_program/taylor-green: test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable taylor-green"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/taylor-green.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/build: test/navier-stokes/reference_program/taylor-green
.PHONY : test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/build

test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program && $(CMAKE_COMMAND) -P CMakeFiles/taylor-green.dir/cmake_clean.cmake
.PHONY : test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/clean

test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/test/navier-stokes/reference_program /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : test/navier-stokes/reference_program/CMakeFiles/taylor-green.dir/depend

