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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials

# Include any dependencies generated for this target.
include c++/exercise/task/CMakeFiles/c++-task3.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include c++/exercise/task/CMakeFiles/c++-task3.dir/compiler_depend.make

# Include the progress variables for this target.
include c++/exercise/task/CMakeFiles/c++-task3.dir/progress.make

# Include the compile flags for this target's objects.
include c++/exercise/task/CMakeFiles/c++-task3.dir/flags.make

c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.o: c++/exercise/task/CMakeFiles/c++-task3.dir/flags.make
c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/exercise/task/task3.cc
c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.o: c++/exercise/task/CMakeFiles/c++-task3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.o -MF CMakeFiles/c++-task3.dir/task3.cc.o.d -o CMakeFiles/c++-task3.dir/task3.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/exercise/task/task3.cc

c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/c++-task3.dir/task3.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/exercise/task/task3.cc > CMakeFiles/c++-task3.dir/task3.cc.i

c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/c++-task3.dir/task3.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/exercise/task/task3.cc -o CMakeFiles/c++-task3.dir/task3.cc.s

# Object files for target c++-task3
c________task3_OBJECTS = \
"CMakeFiles/c++-task3.dir/task3.cc.o"

# External object files for target c++-task3
c________task3_EXTERNAL_OBJECTS =

c++/exercise/task/c++-task3: c++/exercise/task/CMakeFiles/c++-task3.dir/task3.cc.o
c++/exercise/task/c++-task3: c++/exercise/task/CMakeFiles/c++-task3.dir/build.make
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-codegen/lib/libdunecodegen.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab/lib/libdunepdelab.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/lib/libdunealugrid.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
c++/exercise/task/c++-task3: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
c++/exercise/task/c++-task3: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
c++/exercise/task/c++-task3: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
c++/exercise/task/c++-task3: /opt/homebrew/lib/libsuperlu.dylib
c++/exercise/task/c++-task3: /opt/homebrew/lib/libgmp.dylib
c++/exercise/task/c++-task3: /opt/homebrew/lib/libgmpxx.dylib
c++/exercise/task/c++-task3: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
c++/exercise/task/c++-task3: c++/exercise/task/CMakeFiles/c++-task3.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable c++-task3"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/c++-task3.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
c++/exercise/task/CMakeFiles/c++-task3.dir/build: c++/exercise/task/c++-task3
.PHONY : c++/exercise/task/CMakeFiles/c++-task3.dir/build

c++/exercise/task/CMakeFiles/c++-task3.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task && $(CMAKE_COMMAND) -P CMakeFiles/c++-task3.dir/cmake_clean.cmake
.PHONY : c++/exercise/task/CMakeFiles/c++-task3.dir/clean

c++/exercise/task/CMakeFiles/c++-task3.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-pdelab-tutorials/c++/exercise/task /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/c++/exercise/task/CMakeFiles/c++-task3.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : c++/exercise/task/CMakeFiles/c++-task3.dir/depend

