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
include dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/flags.make

dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.o: dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/flags.make
dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/ident/ident.cc
dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.o: dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/ident && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.o -MF CMakeFiles/ident2.dir/ident.cc.o.d -o CMakeFiles/ident2.dir/ident.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/ident/ident.cc

dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ident2.dir/ident.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/ident && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/ident/ident.cc > CMakeFiles/ident2.dir/ident.cc.i

dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ident2.dir/ident.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/ident && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/ident/ident.cc -o CMakeFiles/ident2.dir/ident.cc.s

ident2: dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/ident.cc.o
ident2: dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/build.make
.PHONY : ident2

# Rule to build all files generated by this target.
dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/build: ident2
.PHONY : dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/build

dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/ident && $(CMAKE_COMMAND) -P CMakeFiles/ident2.dir/cmake_clean.cmake
.PHONY : dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/clean

dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/ident /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/ident /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/parallel/ddd/ident/CMakeFiles/ident2.dir/depend
