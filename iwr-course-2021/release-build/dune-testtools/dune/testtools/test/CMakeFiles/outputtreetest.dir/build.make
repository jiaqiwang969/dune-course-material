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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools

# Include any dependencies generated for this target.
include dune/testtools/test/CMakeFiles/outputtreetest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/testtools/test/CMakeFiles/outputtreetest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/testtools/test/CMakeFiles/outputtreetest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/testtools/test/CMakeFiles/outputtreetest.dir/flags.make

dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.o: dune/testtools/test/CMakeFiles/outputtreetest.dir/flags.make
dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/outputtreetest.cc
dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.o: dune/testtools/test/CMakeFiles/outputtreetest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.o -MF CMakeFiles/outputtreetest.dir/outputtreetest.cc.o.d -o CMakeFiles/outputtreetest.dir/outputtreetest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/outputtreetest.cc

dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/outputtreetest.dir/outputtreetest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/outputtreetest.cc > CMakeFiles/outputtreetest.dir/outputtreetest.cc.i

dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/outputtreetest.dir/outputtreetest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/outputtreetest.cc -o CMakeFiles/outputtreetest.dir/outputtreetest.cc.s

# Object files for target outputtreetest
outputtreetest_OBJECTS = \
"CMakeFiles/outputtreetest.dir/outputtreetest.cc.o"

# External object files for target outputtreetest
outputtreetest_EXTERNAL_OBJECTS =

dune/testtools/test/outputtreetest: dune/testtools/test/CMakeFiles/outputtreetest.dir/outputtreetest.cc.o
dune/testtools/test/outputtreetest: dune/testtools/test/CMakeFiles/outputtreetest.dir/build.make
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/testtools/test/outputtreetest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/testtools/test/outputtreetest: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/testtools/test/outputtreetest: /opt/homebrew/lib/libgmp.dylib
dune/testtools/test/outputtreetest: /opt/homebrew/lib/libgmpxx.dylib
dune/testtools/test/outputtreetest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/testtools/test/outputtreetest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/testtools/test/outputtreetest: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/testtools/test/outputtreetest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/testtools/test/outputtreetest: /opt/homebrew/lib/libgmp.dylib
dune/testtools/test/outputtreetest: /opt/homebrew/lib/libgmpxx.dylib
dune/testtools/test/outputtreetest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/testtools/test/outputtreetest: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/testtools/test/outputtreetest: dune/testtools/test/CMakeFiles/outputtreetest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable outputtreetest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/outputtreetest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/testtools/test/CMakeFiles/outputtreetest.dir/build: dune/testtools/test/outputtreetest
.PHONY : dune/testtools/test/CMakeFiles/outputtreetest.dir/build

dune/testtools/test/CMakeFiles/outputtreetest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test && $(CMAKE_COMMAND) -P CMakeFiles/outputtreetest.dir/cmake_clean.cmake
.PHONY : dune/testtools/test/CMakeFiles/outputtreetest.dir/clean

dune/testtools/test/CMakeFiles/outputtreetest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/CMakeFiles/outputtreetest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/testtools/test/CMakeFiles/outputtreetest.dir/depend

