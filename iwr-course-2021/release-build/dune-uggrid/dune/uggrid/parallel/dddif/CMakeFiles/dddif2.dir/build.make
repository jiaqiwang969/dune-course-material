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
include dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/compat.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.o -MF CMakeFiles/dddif2.dir/compat.cc.o.d -o CMakeFiles/dddif2.dir/compat.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/compat.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/compat.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/compat.cc > CMakeFiles/dddif2.dir/compat.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/compat.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/compat.cc -o CMakeFiles/dddif2.dir/compat.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/debugger.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.o -MF CMakeFiles/dddif2.dir/debugger.cc.o.d -o CMakeFiles/dddif2.dir/debugger.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/debugger.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/debugger.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/debugger.cc > CMakeFiles/dddif2.dir/debugger.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/debugger.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/debugger.cc -o CMakeFiles/dddif2.dir/debugger.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/gridcons.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.o -MF CMakeFiles/dddif2.dir/gridcons.cc.o.d -o CMakeFiles/dddif2.dir/gridcons.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/gridcons.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/gridcons.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/gridcons.cc > CMakeFiles/dddif2.dir/gridcons.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/gridcons.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/gridcons.cc -o CMakeFiles/dddif2.dir/gridcons.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/handler.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.o -MF CMakeFiles/dddif2.dir/handler.cc.o.d -o CMakeFiles/dddif2.dir/handler.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/handler.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/handler.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/handler.cc > CMakeFiles/dddif2.dir/handler.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/handler.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/handler.cc -o CMakeFiles/dddif2.dir/handler.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/identify.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.o -MF CMakeFiles/dddif2.dir/identify.cc.o.d -o CMakeFiles/dddif2.dir/identify.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/identify.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/identify.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/identify.cc > CMakeFiles/dddif2.dir/identify.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/identify.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/identify.cc -o CMakeFiles/dddif2.dir/identify.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/initddd.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.o -MF CMakeFiles/dddif2.dir/initddd.cc.o.d -o CMakeFiles/dddif2.dir/initddd.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/initddd.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/initddd.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/initddd.cc > CMakeFiles/dddif2.dir/initddd.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/initddd.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/initddd.cc -o CMakeFiles/dddif2.dir/initddd.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lb.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.o -MF CMakeFiles/dddif2.dir/lb.cc.o.d -o CMakeFiles/dddif2.dir/lb.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lb.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/lb.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lb.cc > CMakeFiles/dddif2.dir/lb.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/lb.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lb.cc -o CMakeFiles/dddif2.dir/lb.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lbrcb.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.o -MF CMakeFiles/dddif2.dir/lbrcb.cc.o.d -o CMakeFiles/dddif2.dir/lbrcb.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lbrcb.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/lbrcb.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lbrcb.cc > CMakeFiles/dddif2.dir/lbrcb.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/lbrcb.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/lbrcb.cc -o CMakeFiles/dddif2.dir/lbrcb.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/memmgr.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_9) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.o -MF CMakeFiles/dddif2.dir/memmgr.cc.o.d -o CMakeFiles/dddif2.dir/memmgr.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/memmgr.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/memmgr.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/memmgr.cc > CMakeFiles/dddif2.dir/memmgr.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/memmgr.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/memmgr.cc -o CMakeFiles/dddif2.dir/memmgr.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/overlap.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_10) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.o -MF CMakeFiles/dddif2.dir/overlap.cc.o.d -o CMakeFiles/dddif2.dir/overlap.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/overlap.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/overlap.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/overlap.cc > CMakeFiles/dddif2.dir/overlap.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/overlap.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/overlap.cc -o CMakeFiles/dddif2.dir/overlap.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/priority.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_11) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.o -MF CMakeFiles/dddif2.dir/priority.cc.o.d -o CMakeFiles/dddif2.dir/priority.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/priority.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/priority.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/priority.cc > CMakeFiles/dddif2.dir/priority.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/priority.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/priority.cc -o CMakeFiles/dddif2.dir/priority.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/pgmcheck.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_12) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.o -MF CMakeFiles/dddif2.dir/pgmcheck.cc.o.d -o CMakeFiles/dddif2.dir/pgmcheck.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/pgmcheck.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/pgmcheck.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/pgmcheck.cc > CMakeFiles/dddif2.dir/pgmcheck.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/pgmcheck.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/pgmcheck.cc -o CMakeFiles/dddif2.dir/pgmcheck.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/partition.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_13) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.o -MF CMakeFiles/dddif2.dir/partition.cc.o.d -o CMakeFiles/dddif2.dir/partition.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/partition.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/partition.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/partition.cc > CMakeFiles/dddif2.dir/partition.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/partition.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/partition.cc -o CMakeFiles/dddif2.dir/partition.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/support.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_14) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.o -MF CMakeFiles/dddif2.dir/support.cc.o.d -o CMakeFiles/dddif2.dir/support.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/support.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/support.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/support.cc > CMakeFiles/dddif2.dir/support.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/support.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/support.cc -o CMakeFiles/dddif2.dir/support.cc.s

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/flags.make
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/trans.cc
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.o: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_15) "Building CXX object dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.o -MF CMakeFiles/dddif2.dir/trans.cc.o.d -o CMakeFiles/dddif2.dir/trans.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/trans.cc

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/dddif2.dir/trans.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/trans.cc > CMakeFiles/dddif2.dir/trans.cc.i

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/dddif2.dir/trans.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif/trans.cc -o CMakeFiles/dddif2.dir/trans.cc.s

dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/compat.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/debugger.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/gridcons.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/handler.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/identify.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/initddd.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lb.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/lbrcb.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/memmgr.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/overlap.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/priority.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/pgmcheck.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/partition.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/support.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/trans.cc.o
dddif2: dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/build.make
.PHONY : dddif2

# Rule to build all files generated by this target.
dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/build: dddif2
.PHONY : dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/build

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif && $(CMAKE_COMMAND) -P CMakeFiles/dddif2.dir/cmake_clean.cmake
.PHONY : dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/clean

dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/dddif /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/parallel/dddif/CMakeFiles/dddif2.dir/depend
