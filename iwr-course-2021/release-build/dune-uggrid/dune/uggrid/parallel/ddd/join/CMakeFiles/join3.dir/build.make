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
include dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/flags.make

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.o: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/flags.make
dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/jcmds.cc
dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.o: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.o -MF CMakeFiles/join3.dir/jcmds.cc.o.d -o CMakeFiles/join3.dir/jcmds.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/jcmds.cc

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/join3.dir/jcmds.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/jcmds.cc > CMakeFiles/join3.dir/jcmds.cc.i

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/join3.dir/jcmds.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/jcmds.cc -o CMakeFiles/join3.dir/jcmds.cc.s

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.o: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/flags.make
dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/join.cc
dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.o: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.o -MF CMakeFiles/join3.dir/join.cc.o.d -o CMakeFiles/join3.dir/join.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/join.cc

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/join3.dir/join.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/join.cc > CMakeFiles/join3.dir/join.cc.i

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/join3.dir/join.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join/join.cc -o CMakeFiles/join3.dir/join.cc.s

join3: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/jcmds.cc.o
join3: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/join.cc.o
join3: dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/build.make
.PHONY : join3

# Rule to build all files generated by this target.
dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/build: join3
.PHONY : dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/build

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join && $(CMAKE_COMMAND) -P CMakeFiles/join3.dir/cmake_clean.cmake
.PHONY : dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/clean

dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/join /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/parallel/ddd/join/CMakeFiles/join3.dir/depend

