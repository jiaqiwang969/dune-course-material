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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions

# Include any dependencies generated for this target.
include examples/CMakeFiles/poisson-mfem.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include examples/CMakeFiles/poisson-mfem.dir/compiler_depend.make

# Include the progress variables for this target.
include examples/CMakeFiles/poisson-mfem.dir/progress.make

# Include the compile flags for this target's objects.
include examples/CMakeFiles/poisson-mfem.dir/flags.make

examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o: examples/CMakeFiles/poisson-mfem.dir/flags.make
examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/examples/poisson-mfem.cc
examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o: examples/CMakeFiles/poisson-mfem.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o -MF CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o.d -o CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/examples/poisson-mfem.cc

examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/examples/poisson-mfem.cc > CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.i

examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/examples/poisson-mfem.cc -o CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.s

# Object files for target poisson-mfem
poisson__mfem_OBJECTS = \
"CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o"

# External object files for target poisson-mfem
poisson__mfem_EXTERNAL_OBJECTS =

examples/poisson-mfem: examples/CMakeFiles/poisson-mfem.dir/poisson-mfem.cc.o
examples/poisson-mfem: examples/CMakeFiles/poisson-mfem.dir/build.make
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
examples/poisson-mfem: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
examples/poisson-mfem: /opt/homebrew/lib/libsuperlu.dylib
examples/poisson-mfem: /opt/homebrew/lib/libgmp.dylib
examples/poisson-mfem: /opt/homebrew/lib/libgmpxx.dylib
examples/poisson-mfem: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
examples/poisson-mfem: examples/CMakeFiles/poisson-mfem.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable poisson-mfem"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/poisson-mfem.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
examples/CMakeFiles/poisson-mfem.dir/build: examples/poisson-mfem
.PHONY : examples/CMakeFiles/poisson-mfem.dir/build

examples/CMakeFiles/poisson-mfem.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples && $(CMAKE_COMMAND) -P CMakeFiles/poisson-mfem.dir/cmake_clean.cmake
.PHONY : examples/CMakeFiles/poisson-mfem.dir/clean

examples/CMakeFiles/poisson-mfem.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-functions/examples /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/examples/CMakeFiles/poisson-mfem.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : examples/CMakeFiles/poisson-mfem.dir/depend

