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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions

# Include any dependencies generated for this target.
include dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/flags.make

dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o: dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/flags.make
dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/dune/localfunctions/test/raviartthomaselementtest.cc
dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o: dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o -MF CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o.d -o CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/dune/localfunctions/test/raviartthomaselementtest.cc

dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/dune/localfunctions/test/raviartthomaselementtest.cc > CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.i

dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/dune/localfunctions/test/raviartthomaselementtest.cc -o CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.s

# Object files for target raviartthomaselementtest
raviartthomaselementtest_OBJECTS = \
"CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o"

# External object files for target raviartthomaselementtest
raviartthomaselementtest_EXTERNAL_OBJECTS =

dune/localfunctions/test/raviartthomaselementtest: dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/raviartthomaselementtest.cc.o
dune/localfunctions/test/raviartthomaselementtest: dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/build.make
dune/localfunctions/test/raviartthomaselementtest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/localfunctions/test/raviartthomaselementtest: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/localfunctions/test/raviartthomaselementtest: /opt/homebrew/lib/libgmp.dylib
dune/localfunctions/test/raviartthomaselementtest: /opt/homebrew/lib/libgmpxx.dylib
dune/localfunctions/test/raviartthomaselementtest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/localfunctions/test/raviartthomaselementtest: dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable raviartthomaselementtest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/raviartthomaselementtest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/build: dune/localfunctions/test/raviartthomaselementtest
.PHONY : dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/build

dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test && $(CMAKE_COMMAND) -P CMakeFiles/raviartthomaselementtest.dir/cmake_clean.cmake
.PHONY : dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/clean

dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-localfunctions/dune/localfunctions/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-localfunctions/dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/localfunctions/test/CMakeFiles/raviartthomaselementtest.dir/depend

