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
include dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmds.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.o -MF CMakeFiles/xfer3.dir/cmds.cc.o.d -o CMakeFiles/xfer3.dir/cmds.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmds.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/cmds.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmds.cc > CMakeFiles/xfer3.dir/cmds.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/cmds.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmds.cc -o CMakeFiles/xfer3.dir/cmds.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmdmsg.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.o -MF CMakeFiles/xfer3.dir/cmdmsg.cc.o.d -o CMakeFiles/xfer3.dir/cmdmsg.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmdmsg.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/cmdmsg.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmdmsg.cc > CMakeFiles/xfer3.dir/cmdmsg.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/cmdmsg.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cmdmsg.cc -o CMakeFiles/xfer3.dir/cmdmsg.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cplmsg.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.o -MF CMakeFiles/xfer3.dir/cplmsg.cc.o.d -o CMakeFiles/xfer3.dir/cplmsg.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cplmsg.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/cplmsg.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cplmsg.cc > CMakeFiles/xfer3.dir/cplmsg.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/cplmsg.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/cplmsg.cc -o CMakeFiles/xfer3.dir/cplmsg.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/ctrl.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.o -MF CMakeFiles/xfer3.dir/ctrl.cc.o.d -o CMakeFiles/xfer3.dir/ctrl.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/ctrl.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/ctrl.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/ctrl.cc > CMakeFiles/xfer3.dir/ctrl.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/ctrl.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/ctrl.cc -o CMakeFiles/xfer3.dir/ctrl.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/pack.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.o -MF CMakeFiles/xfer3.dir/pack.cc.o.d -o CMakeFiles/xfer3.dir/pack.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/pack.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/pack.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/pack.cc > CMakeFiles/xfer3.dir/pack.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/pack.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/pack.cc -o CMakeFiles/xfer3.dir/pack.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/supp.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_6) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.o -MF CMakeFiles/xfer3.dir/supp.cc.o.d -o CMakeFiles/xfer3.dir/supp.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/supp.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/supp.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/supp.cc > CMakeFiles/xfer3.dir/supp.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/supp.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/supp.cc -o CMakeFiles/xfer3.dir/supp.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/unpack.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_7) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.o -MF CMakeFiles/xfer3.dir/unpack.cc.o.d -o CMakeFiles/xfer3.dir/unpack.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/unpack.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/unpack.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/unpack.cc > CMakeFiles/xfer3.dir/unpack.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/unpack.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/unpack.cc -o CMakeFiles/xfer3.dir/unpack.cc.s

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/flags.make
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/xfer.cc
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.o: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_8) "Building CXX object dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.o -MF CMakeFiles/xfer3.dir/xfer.cc.o.d -o CMakeFiles/xfer3.dir/xfer.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/xfer.cc

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/xfer3.dir/xfer.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/xfer.cc > CMakeFiles/xfer3.dir/xfer.cc.i

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/xfer3.dir/xfer.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer/xfer.cc -o CMakeFiles/xfer3.dir/xfer.cc.s

xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmds.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cmdmsg.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/cplmsg.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/ctrl.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/pack.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/supp.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/unpack.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/xfer.cc.o
xfer3: dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/build.make
.PHONY : xfer3

# Rule to build all files generated by this target.
dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/build: xfer3
.PHONY : dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/build

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer && $(CMAKE_COMMAND) -P CMakeFiles/xfer3.dir/cmake_clean.cmake
.PHONY : dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/clean

dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/xfer /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/parallel/ddd/xfer/CMakeFiles/xfer3.dir/depend
