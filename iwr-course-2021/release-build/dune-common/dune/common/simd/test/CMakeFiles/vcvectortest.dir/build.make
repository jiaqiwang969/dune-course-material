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
CMAKE_SOURCE_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common

# Include any dependencies generated for this target.
include dune/common/simd/test/CMakeFiles/vcvectortest.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include dune/common/simd/test/CMakeFiles/vcvectortest.dir/compiler_depend.make

# Include the progress variables for this target.
include dune/common/simd/test/CMakeFiles/vcvectortest.dir/progress.make

# Include the compile flags for this target's objects.
include dune/common/simd/test/CMakeFiles/vcvectortest.dir/flags.make

dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o: dune/common/simd/test/CMakeFiles/vcvectortest.dir/flags.make
dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o: dune/common/simd/test/main77_vcvectortest.cc
dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o: dune/common/simd/test/CMakeFiles/vcvectortest.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o -MF CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o.d -o CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o -c /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test/main77_vcvectortest.cc

dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.i"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test/main77_vcvectortest.cc > CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.i

dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.s"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test && /usr/bin/g++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test/main77_vcvectortest.cc -o CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.s

# Object files for target vcvectortest
vcvectortest_OBJECTS = \
"CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o"

# External object files for target vcvectortest
vcvectortest_EXTERNAL_OBJECTS =

dune/common/simd/test/vcvectortest: dune/common/simd/test/CMakeFiles/vcvectortest.dir/main77_vcvectortest.cc.o
dune/common/simd/test/vcvectortest: dune/common/simd/test/CMakeFiles/vcvectortest.dir/build.make
dune/common/simd/test/vcvectortest: /opt/homebrew/lib/libgmp.dylib
dune/common/simd/test/vcvectortest: /opt/homebrew/lib/libgmpxx.dylib
dune/common/simd/test/vcvectortest: /opt/homebrew/Cellar/open-mpi/4.1.1_2/lib/libmpi.dylib
dune/common/simd/test/vcvectortest: lib/libdunecommon.a
dune/common/simd/test/vcvectortest: dune/common/simd/test/CMakeFiles/vcvectortest.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable vcvectortest"
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/vcvectortest.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
dune/common/simd/test/CMakeFiles/vcvectortest.dir/build: dune/common/simd/test/vcvectortest
.PHONY : dune/common/simd/test/CMakeFiles/vcvectortest.dir/build

dune/common/simd/test/CMakeFiles/vcvectortest.dir/clean:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test && $(CMAKE_COMMAND) -P CMakeFiles/vcvectortest.dir/cmake_clean.cmake
.PHONY : dune/common/simd/test/CMakeFiles/vcvectortest.dir/clean

dune/common/simd/test/CMakeFiles/vcvectortest.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/dune/dune-common/dune/common/simd/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-common/dune/common/simd/test/CMakeFiles/vcvectortest.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : dune/common/simd/test/CMakeFiles/vcvectortest.dir/depend

