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
include examples/communication/CMakeFiles/main_transport_comm.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/communication/CMakeFiles/main_transport_comm.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/communication/CMakeFiles/main_transport_comm.dir/progress.make

# Include the compile flags for this target's objects.
include examples/communication/CMakeFiles/main_transport_comm.dir/flags.make

examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.o: examples/communication/CMakeFiles/main_transport_comm.dir/flags.make
examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/communication/main.cc
examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.o: examples/communication/CMakeFiles/main_transport_comm.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.o -MF CMakeFiles/main_transport_comm.dir/main.cc.o.d -o CMakeFiles/main_transport_comm.dir/main.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/communication/main.cc

examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/main_transport_comm.dir/main.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/communication/main.cc > CMakeFiles/main_transport_comm.dir/main.cc.i

examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/main_transport_comm.dir/main.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/communication/main.cc -o CMakeFiles/main_transport_comm.dir/main.cc.s

# Object files for target main_transport_comm
main_transport_comm_OBJECTS = \
"CMakeFiles/main_transport_comm.dir/main.cc.o"

# External object files for target main_transport_comm
main_transport_comm_EXTERNAL_OBJECTS =

examples/communication/main_transport_comm: examples/communication/CMakeFiles/main_transport_comm.dir/main.cc.o
examples/communication/main_transport_comm: examples/communication/CMakeFiles/main_transport_comm.dir/build.make
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/communication/main_transport_comm: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/communication/main_transport_comm: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/communication/main_transport_comm: /opt/homebrew/lib/libgmp.dylib
examples/communication/main_transport_comm: /opt/homebrew/lib/libgmpxx.dylib
examples/communication/main_transport_comm: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/communication/main_transport_comm: lib/libdunealugrid.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/communication/main_transport_comm: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/communication/main_transport_comm: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/communication/main_transport_comm: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
examples/communication/main_transport_comm: examples/communication/CMakeFiles/main_transport_comm.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable main_transport_comm"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/main_transport_comm.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/communication/CMakeFiles/main_transport_comm.dir/build: examples/communication/main_transport_comm
.PHONY : examples/communication/CMakeFiles/main_transport_comm.dir/build

examples/communication/CMakeFiles/main_transport_comm.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication && $(CMAKE_COMMAND) -P CMakeFiles/main_transport_comm.dir/cmake_clean.cmake
.PHONY : examples/communication/CMakeFiles/main_transport_comm.dir/clean

examples/communication/CMakeFiles/main_transport_comm.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/communication /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/communication/CMakeFiles/main_transport_comm.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/communication/CMakeFiles/main_transport_comm.dir/depend

