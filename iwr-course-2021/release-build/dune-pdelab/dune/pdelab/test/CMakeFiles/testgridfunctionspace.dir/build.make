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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab

# Include any dependencies generated for this target.
include dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/progress.make

# Include the compile flags for this target's objects.
include dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/flags.make

dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o: dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/flags.make
dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testgridfunctionspace.cc
dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o: dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o -MF CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o.d -o CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testgridfunctionspace.cc

dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testgridfunctionspace.cc > CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.i

dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test/testgridfunctionspace.cc -o CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.s

# Object files for target testgridfunctionspace
testgridfunctionspace_OBJECTS = \
"CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o"

# External object files for target testgridfunctionspace
testgridfunctionspace_EXTERNAL_OBJECTS =

dune/pdelab/test/testgridfunctionspace: dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/testgridfunctionspace.cc.o
dune/pdelab/test/testgridfunctionspace: dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/build.make
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testgridfunctionspace: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/lib/libsuperlu.dylib
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/lib/libgmp.dylib
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/lib/libgmpxx.dylib
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testgridfunctionspace: lib/libdunepdelab.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testgridfunctionspace: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/lib/libsuperlu.dylib
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/pdelab/test/testgridfunctionspace: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/lib/libgmp.dylib
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/lib/libgmpxx.dylib
dune/pdelab/test/testgridfunctionspace: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/pdelab/test/testgridfunctionspace: dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable testgridfunctionspace"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/testgridfunctionspace.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/build: dune/pdelab/test/testgridfunctionspace
.PHONY : dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/build

dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test && $(CMAKE_COMMAND) -P CMakeFiles/testgridfunctionspace.dir/cmake_clean.cmake
.PHONY : dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/clean

dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/dune/pdelab/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/pdelab/test/CMakeFiles/testgridfunctionspace.dir/depend

