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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid

# Include any dependencies generated for this target.
include dune/alugrid/test/CMakeFiles/test-backup-restore.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/alugrid/test/CMakeFiles/test-backup-restore.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/alugrid/test/CMakeFiles/test-backup-restore.dir/progress.make

# Include the compile flags for this target's objects.
include dune/alugrid/test/CMakeFiles/test-backup-restore.dir/flags.make

dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o: dune/alugrid/test/CMakeFiles/test-backup-restore.dir/flags.make
dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/dune/alugrid/test/test-backup-restore.cc
dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o: dune/alugrid/test/CMakeFiles/test-backup-restore.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o -MF CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o.d -o CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/dune/alugrid/test/test-backup-restore.cc

dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/dune/alugrid/test/test-backup-restore.cc > CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.i

dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/dune/alugrid/test/test-backup-restore.cc -o CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.s

# Object files for target test-backup-restore
test__backup__restore_OBJECTS = \
"CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o"

# External object files for target test-backup-restore
test__backup__restore_EXTERNAL_OBJECTS =

dune/alugrid/test/test-backup-restore: dune/alugrid/test/CMakeFiles/test-backup-restore.dir/test-backup-restore.cc.o
dune/alugrid/test/test-backup-restore: dune/alugrid/test/CMakeFiles/test-backup-restore.dir/build.make
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/alugrid/test/test-backup-restore: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/alugrid/test/test-backup-restore: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/alugrid/test/test-backup-restore: /opt/homebrew/lib/libgmp.dylib
dune/alugrid/test/test-backup-restore: /opt/homebrew/lib/libgmpxx.dylib
dune/alugrid/test/test-backup-restore: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/alugrid/test/test-backup-restore: lib/libdunealugrid.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-grid/lib/libdunegrid.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-geometry/lib/libdunegeometry.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS3.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugS2.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-uggrid/lib/libugL.a
dune/alugrid/test/test-backup-restore: /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/lib/libdunecommon.a
dune/alugrid/test/test-backup-restore: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/alugrid/test/test-backup-restore: /Library/Developer/CommandLineTools/SDKs/MacOSX11.3.sdk/usr/lib/libz.tbd
dune/alugrid/test/test-backup-restore: dune/alugrid/test/CMakeFiles/test-backup-restore.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable test-backup-restore"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/test-backup-restore.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/alugrid/test/CMakeFiles/test-backup-restore.dir/build: dune/alugrid/test/test-backup-restore
.PHONY : dune/alugrid/test/CMakeFiles/test-backup-restore.dir/build

dune/alugrid/test/CMakeFiles/test-backup-restore.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test && $(CMAKE_COMMAND) -P CMakeFiles/test-backup-restore.dir/cmake_clean.cmake
.PHONY : dune/alugrid/test/CMakeFiles/test-backup-restore.dir/clean

dune/alugrid/test/CMakeFiles/test-backup-restore.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-alugrid/dune/alugrid/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-alugrid/dune/alugrid/test/CMakeFiles/test-backup-restore.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/alugrid/test/CMakeFiles/test-backup-restore.dir/depend
