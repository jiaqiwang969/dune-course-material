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
include examples/quality/CMakeFiles/main_quality.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/quality/CMakeFiles/main_quality.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/quality/CMakeFiles/main_quality.dir/progress.make

# Include the compile flags for this target's objects.
include examples/quality/CMakeFiles/main_quality.dir/flags.make

examples/quality/CMakeFiles/main_quality.dir/main.cc.o: examples/quality/CMakeFiles/main_quality.dir/flags.make
examples/quality/CMakeFiles/main_quality.dir/main.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/quality/main.cc
examples/quality/CMakeFiles/main_quality.dir/main.cc.o: examples/quality/CMakeFiles/main_quality.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/quality/CMakeFiles/main_quality.dir/main.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/quality/CMakeFiles/main_quality.dir/main.cc.o -MF CMakeFiles/main_quality.dir/main.cc.o.d -o CMakeFiles/main_quality.dir/main.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/quality/main.cc

examples/quality/CMakeFiles/main_quality.dir/main.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/main_quality.dir/main.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/quality/main.cc > CMakeFiles/main_quality.dir/main.cc.i

examples/quality/CMakeFiles/main_quality.dir/main.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/main_quality.dir/main.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/quality/main.cc -o CMakeFiles/main_quality.dir/main.cc.s

# Object files for target main_quality
main_quality_OBJECTS = \
"CMakeFiles/main_quality.dir/main.cc.o"

# External object files for target main_quality
main_quality_EXTERNAL_OBJECTS =

examples/quality/main_quality: examples/quality/CMakeFiles/main_quality.dir/main.cc.o
examples/quality/main_quality: examples/quality/CMakeFiles/main_quality.dir/build.make
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/quality/main_quality: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/quality/main_quality: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/quality/main_quality: /opt/homebrew/lib/libgmp.dylib
examples/quality/main_quality: /opt/homebrew/lib/libgmpxx.dylib
examples/quality/main_quality: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/quality/main_quality: lib/libdunealugrid.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/quality/main_quality: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/quality/main_quality: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/quality/main_quality: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
examples/quality/main_quality: examples/quality/CMakeFiles/main_quality.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable main_quality"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/main_quality.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/quality/CMakeFiles/main_quality.dir/build: examples/quality/main_quality
.PHONY : examples/quality/CMakeFiles/main_quality.dir/build

examples/quality/CMakeFiles/main_quality.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality && $(CMAKE_COMMAND) -P CMakeFiles/main_quality.dir/cmake_clean.cmake
.PHONY : examples/quality/CMakeFiles/main_quality.dir/clean

examples/quality/CMakeFiles/main_quality.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/examples/quality /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/examples/quality/CMakeFiles/main_quality.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/quality/CMakeFiles/main_quality.dir/depend
