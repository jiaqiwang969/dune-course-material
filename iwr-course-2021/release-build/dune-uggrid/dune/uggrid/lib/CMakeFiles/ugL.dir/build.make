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
include dune/uggrid/lib/CMakeFiles/ugL.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/uggrid/lib/CMakeFiles/ugL.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/uggrid/lib/CMakeFiles/ugL.dir/progress.make

# Include the compile flags for this target's objects.
include dune/uggrid/lib/CMakeFiles/ugL.dir/flags.make

dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o: dune/uggrid/lib/CMakeFiles/ugL.dir/flags.make
dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/dddcontext.cc
dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o: dune/uggrid/lib/CMakeFiles/ugL.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o -MF CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o.d -o CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/dddcontext.cc

dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/dddcontext.cc > CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.i

dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ddd/dddcontext.cc -o CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.s

dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o: dune/uggrid/lib/CMakeFiles/ugL.dir/flags.make
dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppifcontext.cc
dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o: dune/uggrid/lib/CMakeFiles/ugL.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building CXX object dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o -MF CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o.d -o CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppifcontext.cc

dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppifcontext.cc > CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.i

dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/parallel/ppif/ppifcontext.cc -o CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.s

# Object files for target ugL
ugL_OBJECTS = \
"CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o" \
"CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o"

# External object files for target ugL
ugL_EXTERNAL_OBJECTS = \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/CMakeFiles/devices.dir/ugdevices.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/ugenv.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/heaps.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/fifo.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/misc.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/defaults.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/initlow.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/fileopen.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/ugstruct.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/debug.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/bio.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/scan.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/low/CMakeFiles/low.dir/ugtimer.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o" \
"/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o"

lib/libugL.a: dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ddd/dddcontext.cc.o
lib/libugL.a: dune/uggrid/lib/CMakeFiles/ugL.dir/__/parallel/ppif/ppifcontext.cc.o
lib/libugL.a: dune/uggrid/CMakeFiles/devices.dir/ugdevices.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/ugenv.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/heaps.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/fifo.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/misc.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/defaults.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/initlow.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/fileopen.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/ugstruct.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/debug.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/bio.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/scan.cc.o
lib/libugL.a: dune/uggrid/low/CMakeFiles/low.dir/ugtimer.cc.o
lib/libugL.a: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/io.cc.o
lib/libugL.a: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/lowcomm.cc.o
lib/libugL.a: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/notify.cc.o
lib/libugL.a: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/reduct.cc.o
lib/libugL.a: dune/uggrid/parallel/ddd/basic/CMakeFiles/basic.dir/topo.cc.o
lib/libugL.a: dune/uggrid/parallel/ppif/CMakeFiles/ppifmpi.dir/ppif.cc.o
lib/libugL.a: dune/uggrid/lib/CMakeFiles/ugL.dir/build.make
lib/libugL.a: dune/uggrid/lib/CMakeFiles/ugL.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Linking CXX static library ../../../lib/libugL.a"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && $(CMAKE_COMMAND) -P CMakeFiles/ugL.dir/cmake_clean_target.cmake
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/ugL.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/uggrid/lib/CMakeFiles/ugL.dir/build: lib/libugL.a
.PHONY : dune/uggrid/lib/CMakeFiles/ugL.dir/build

dune/uggrid/lib/CMakeFiles/ugL.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib && $(CMAKE_COMMAND) -P CMakeFiles/ugL.dir/cmake_clean.cmake
.PHONY : dune/uggrid/lib/CMakeFiles/ugL.dir/clean

dune/uggrid/lib/CMakeFiles/ugL.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-uggrid/dune/uggrid/lib /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/dune/uggrid/lib/CMakeFiles/ugL.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/uggrid/lib/CMakeFiles/ugL.dir/depend

