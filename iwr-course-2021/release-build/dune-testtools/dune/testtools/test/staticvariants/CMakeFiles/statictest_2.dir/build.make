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
include dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/progress.make

# Include the compile flags for this target's objects.
include dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/flags.make

dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.o: dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/flags.make
dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/staticvariants/source.cc
dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.o: dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.o -MF CMakeFiles/statictest_2.dir/source.cc.o.d -o CMakeFiles/statictest_2.dir/source.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/staticvariants/source.cc

dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/statictest_2.dir/source.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/staticvariants/source.cc > CMakeFiles/statictest_2.dir/source.cc.i

dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/statictest_2.dir/source.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/staticvariants/source.cc -o CMakeFiles/statictest_2.dir/source.cc.s

# Object files for target statictest_2
statictest_2_OBJECTS = \
"CMakeFiles/statictest_2.dir/source.cc.o"

# External object files for target statictest_2
statictest_2_EXTERNAL_OBJECTS =

dune/testtools/test/staticvariants/statictest_2: dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/source.cc.o
dune/testtools/test/staticvariants/statictest_2: dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/build.make
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/testtools/test/staticvariants/statictest_2: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/testtools/test/staticvariants/statictest_2: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/testtools/test/staticvariants/statictest_2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/testtools/test/staticvariants/statictest_2: /opt/homebrew/lib/libgmp.dylib
dune/testtools/test/staticvariants/statictest_2: /opt/homebrew/lib/libgmpxx.dylib
dune/testtools/test/staticvariants/statictest_2: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/testtools/test/staticvariants/statictest_2: dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable statictest_2"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/statictest_2.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/build: dune/testtools/test/staticvariants/statictest_2
.PHONY : dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/build

dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants && $(CMAKE_COMMAND) -P CMakeFiles/statictest_2.dir/cmake_clean.cmake
.PHONY : dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/clean

dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-testtools/dune/testtools/test/staticvariants /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-testtools/dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/testtools/test/staticvariants/CMakeFiles/statictest_2.dir/depend

