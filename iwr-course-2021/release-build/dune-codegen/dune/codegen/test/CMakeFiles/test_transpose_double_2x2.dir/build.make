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
include dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/progress.make

# Include the compile flags for this target's objects.
include dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/flags.make

dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o: dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/flags.make
dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/dune/codegen/test/test_transpose.cc
dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o: dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o -MF CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o.d -o CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/dune/codegen/test/test_transpose.cc

dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/dune/codegen/test/test_transpose.cc > CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.i

dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/dune/codegen/test/test_transpose.cc -o CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.s

# Object files for target test_transpose_double_2x2
test_transpose_double_2x2_OBJECTS = \
"CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o"

# External object files for target test_transpose_double_2x2
test_transpose_double_2x2_EXTERNAL_OBJECTS =

dune/codegen/test/test_transpose_double_2x2: dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/test_transpose.cc.o
dune/codegen/test/test_transpose_double_2x2: dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/build.make
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/lib/libdunepdelab.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/codegen/test/test_transpose_double_2x2: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/lib/libsuperlu.dylib
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/lib/libgmp.dylib
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/lib/libgmpxx.dylib
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/codegen/test/test_transpose_double_2x2: lib/libdunecodegen.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/lib/libdunepdelab.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/codegen/test/test_transpose_double_2x2: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/codegen/test/test_transpose_double_2x2: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/lib/libsuperlu.dylib
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/lib/libgmp.dylib
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/lib/libgmpxx.dylib
dune/codegen/test/test_transpose_double_2x2: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/codegen/test/test_transpose_double_2x2: dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test_transpose_double_2x2"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test_transpose_double_2x2.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/build: dune/codegen/test/test_transpose_double_2x2
.PHONY : dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/build

dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test && $(CMAKE_COMMAND) -P CMakeFiles/test_transpose_double_2x2.dir/cmake_clean.cmake
.PHONY : dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/clean

dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-codegen/dune/codegen/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/codegen/test/CMakeFiles/test_transpose_double_2x2.dir/depend

