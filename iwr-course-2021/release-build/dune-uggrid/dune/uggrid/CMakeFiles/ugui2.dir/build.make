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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid

# Include any dependencies generated for this target.
include dune/uggrid/CMakeFiles/ugui2.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/CMakeFiles/ugui2.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/CMakeFiles/ugui2.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/CMakeFiles/ugui2.dir/flags.make

dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.o: dune/uggrid/CMakeFiles/ugui2.dir/flags.make
dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/ugdevices.cc
dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.o: dune/uggrid/CMakeFiles/ugui2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.o -MF CMakeFiles/ugui2.dir/ugdevices.cc.o.d -o CMakeFiles/ugui2.dir/ugdevices.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/ugdevices.cc

dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ugui2.dir/ugdevices.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/ugdevices.cc > CMakeFiles/ugui2.dir/ugdevices.cc.i

dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ugui2.dir/ugdevices.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/ugdevices.cc -o CMakeFiles/ugui2.dir/ugdevices.cc.s

dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.o: dune/uggrid/CMakeFiles/ugui2.dir/flags.make
dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/commands.cc
dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.o: dune/uggrid/CMakeFiles/ugui2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.o -MF CMakeFiles/ugui2.dir/commands.cc.o.d -o CMakeFiles/ugui2.dir/commands.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/commands.cc

dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ugui2.dir/commands.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/commands.cc > CMakeFiles/ugui2.dir/commands.cc.i

dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ugui2.dir/commands.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/commands.cc -o CMakeFiles/ugui2.dir/commands.cc.s

ugui2: dune/uggrid/CMakeFiles/ugui2.dir/ugdevices.cc.o
ugui2: dune/uggrid/CMakeFiles/ugui2.dir/commands.cc.o
ugui2: dune/uggrid/CMakeFiles/ugui2.dir/build.make
.PHONY : ugui2

# Rule to build all files generated by this target.
dune/uggrid/CMakeFiles/ugui2.dir/build: ugui2
.PHONY : dune/uggrid/CMakeFiles/ugui2.dir/build

dune/uggrid/CMakeFiles/ugui2.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid && $(CMAKE_COMMAND) -P CMakeFiles/ugui2.dir/cmake_clean.cmake
.PHONY : dune/uggrid/CMakeFiles/ugui2.dir/clean

dune/uggrid/CMakeFiles/ugui2.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/CMakeFiles/ugui2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/CMakeFiles/ugui2.dir/depend

