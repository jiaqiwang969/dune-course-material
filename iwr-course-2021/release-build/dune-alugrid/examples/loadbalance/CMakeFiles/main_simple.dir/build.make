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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid

# Include any dependencies generated for this target.
include examples/loadbalance/CMakeFiles/main_simple.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/loadbalance/CMakeFiles/main_simple.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/loadbalance/CMakeFiles/main_simple.dir/progress.make

# Include the compile flags for this target's objects.
include examples/loadbalance/CMakeFiles/main_simple.dir/flags.make

examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.o: examples/loadbalance/CMakeFiles/main_simple.dir/flags.make
examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/loadbalance/main.cc
examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.o: examples/loadbalance/CMakeFiles/main_simple.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.o -MF CMakeFiles/main_simple.dir/main.cc.o.d -o CMakeFiles/main_simple.dir/main.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/loadbalance/main.cc

examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/main_simple.dir/main.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/loadbalance/main.cc > CMakeFiles/main_simple.dir/main.cc.i

examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/main_simple.dir/main.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/loadbalance/main.cc -o CMakeFiles/main_simple.dir/main.cc.s

# Object files for target main_simple
main_simple_OBJECTS = \
"CMakeFiles/main_simple.dir/main.cc.o"

# External object files for target main_simple
main_simple_EXTERNAL_OBJECTS =

examples/loadbalance/main_simple: examples/loadbalance/CMakeFiles/main_simple.dir/main.cc.o
examples/loadbalance/main_simple: examples/loadbalance/CMakeFiles/main_simple.dir/build.make
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/loadbalance/main_simple: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/loadbalance/main_simple: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/loadbalance/main_simple: /opt/homebrew/lib/libgmp.dylib
examples/loadbalance/main_simple: /opt/homebrew/lib/libgmpxx.dylib
examples/loadbalance/main_simple: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/loadbalance/main_simple: lib/libdunealugrid.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/loadbalance/main_simple: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/loadbalance/main_simple: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/loadbalance/main_simple: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
examples/loadbalance/main_simple: examples/loadbalance/CMakeFiles/main_simple.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable main_simple"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/main_simple.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/loadbalance/CMakeFiles/main_simple.dir/build: examples/loadbalance/main_simple
.PHONY : examples/loadbalance/CMakeFiles/main_simple.dir/build

examples/loadbalance/CMakeFiles/main_simple.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance && $(CMAKE_COMMAND) -P CMakeFiles/main_simple.dir/cmake_clean.cmake
.PHONY : examples/loadbalance/CMakeFiles/main_simple.dir/clean

examples/loadbalance/CMakeFiles/main_simple.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/loadbalance /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/loadbalance/CMakeFiles/main_simple.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/loadbalance/CMakeFiles/main_simple.dir/depend

