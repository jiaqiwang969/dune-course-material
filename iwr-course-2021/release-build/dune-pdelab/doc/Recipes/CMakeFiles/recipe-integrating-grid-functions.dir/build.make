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
include doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/compiler_depend.make

# Include the progress variables for this target.
include doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/progress.make

# Include the compile flags for this target's objects.
include doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/flags.make

doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o: doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/flags.make
doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/doc/Recipes/recipe-integrating-grid-functions.cc
doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o: doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o -MF CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o.d -o CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/doc/Recipes/recipe-integrating-grid-functions.cc

doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/doc/Recipes/recipe-integrating-grid-functions.cc > CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.i

doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/doc/Recipes/recipe-integrating-grid-functions.cc -o CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.s

# Object files for target recipe-integrating-grid-functions
recipe__integrating__grid__functions_OBJECTS = \
"CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o"

# External object files for target recipe-integrating-grid-functions
recipe__integrating__grid__functions_EXTERNAL_OBJECTS =

doc/Recipes/recipe-integrating-grid-functions: doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/recipe-integrating-grid-functions.cc.o
doc/Recipes/recipe-integrating-grid-functions: doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/build.make
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
doc/Recipes/recipe-integrating-grid-functions: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/lib/libsuperlu.dylib
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/lib/libgmp.dylib
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/lib/libgmpxx.dylib
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
doc/Recipes/recipe-integrating-grid-functions: lib/libdunepdelab.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
doc/Recipes/recipe-integrating-grid-functions: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/lib/libsuperlu.dylib
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
doc/Recipes/recipe-integrating-grid-functions: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/lib/libgmp.dylib
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/lib/libgmpxx.dylib
doc/Recipes/recipe-integrating-grid-functions: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
doc/Recipes/recipe-integrating-grid-functions: doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable recipe-integrating-grid-functions"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/recipe-integrating-grid-functions.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/build: doc/Recipes/recipe-integrating-grid-functions
.PHONY : doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/build

doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes && $(CMAKE_COMMAND) -P CMakeFiles/recipe-integrating-grid-functions.dir/cmake_clean.cmake
.PHONY : doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/clean

doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab/doc/Recipes /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : doc/Recipes/CMakeFiles/recipe-integrating-grid-functions.dir/depend

