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
include dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/flags.make

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/flags.make
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/io.cc
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o -MF CMakeFiles/basic.dir/io.cc.o.d -o CMakeFiles/basic.dir/io.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/io.cc

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/basic.dir/io.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/io.cc > CMakeFiles/basic.dir/io.cc.i

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/basic.dir/io.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/io.cc -o CMakeFiles/basic.dir/io.cc.s

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/flags.make
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/lowcomm.cc
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o -MF CMakeFiles/basic.dir/lowcomm.cc.o.d -o CMakeFiles/basic.dir/lowcomm.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/lowcomm.cc

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/basic.dir/lowcomm.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/lowcomm.cc > CMakeFiles/basic.dir/lowcomm.cc.i

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/basic.dir/lowcomm.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/lowcomm.cc -o CMakeFiles/basic.dir/lowcomm.cc.s

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/flags.make
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/notify.cc
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o -MF CMakeFiles/basic.dir/notify.cc.o.d -o CMakeFiles/basic.dir/notify.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/notify.cc

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/basic.dir/notify.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/notify.cc > CMakeFiles/basic.dir/notify.cc.i

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/basic.dir/notify.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/notify.cc -o CMakeFiles/basic.dir/notify.cc.s

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/flags.make
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/reduct.cc
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o -MF CMakeFiles/basic.dir/reduct.cc.o.d -o CMakeFiles/basic.dir/reduct.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/reduct.cc

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/basic.dir/reduct.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/reduct.cc > CMakeFiles/basic.dir/reduct.cc.i

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/basic.dir/reduct.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/reduct.cc -o CMakeFiles/basic.dir/reduct.cc.s

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/flags.make
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/topo.cc
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o -MF CMakeFiles/basic.dir/topo.cc.o.d -o CMakeFiles/basic.dir/topo.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/topo.cc

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/basic.dir/topo.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/topo.cc > CMakeFiles/basic.dir/topo.cc.i

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/basic.dir/topo.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic/topo.cc -o CMakeFiles/basic.dir/topo.cc.s

basic: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o
basic: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o
basic: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o
basic: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o
basic: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o
basic: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/build.make
.PHONY : basic

# Rule to build all files generated by this target.
dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/build: basic
.PHONY : dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/build

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic && $(CMAKE_COMMAND) -P CMakeFiles/basic.dir/cmake_clean.cmake
.PHONY : dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/clean

dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/basic /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/depend

