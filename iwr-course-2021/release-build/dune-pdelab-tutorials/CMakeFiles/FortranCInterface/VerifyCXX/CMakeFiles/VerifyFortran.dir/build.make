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

# Produce verbose output by default.
VERBOSE = 1

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
CMAKE_SOURCE_DIR = /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX

# Include any dependencies generated for this target.
include CMakeFiles/VerifyFortran.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/VerifyFortran.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/VerifyFortran.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/VerifyFortran.dir/flags.make

CMakeFiles/VerifyFortran.dir/VerifyFortran.f.o: CMakeFiles/VerifyFortran.dir/flags.make
CMakeFiles/VerifyFortran.dir/VerifyFortran.f.o: /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify/VerifyFortran.f
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building Fortran object CMakeFiles/VerifyFortran.dir/VerifyFortran.f.o"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -c /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify/VerifyFortran.f -o CMakeFiles/VerifyFortran.dir/VerifyFortran.f.o

CMakeFiles/VerifyFortran.dir/VerifyFortran.f.i: cmake_force
	@echo "Preprocessing Fortran source to CMakeFiles/VerifyFortran.dir/VerifyFortran.f.i"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -E /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify/VerifyFortran.f > CMakeFiles/VerifyFortran.dir/VerifyFortran.f.i

CMakeFiles/VerifyFortran.dir/VerifyFortran.f.s: cmake_force
	@echo "Compiling Fortran source to assembly CMakeFiles/VerifyFortran.dir/VerifyFortran.f.s"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -S /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify/VerifyFortran.f -o CMakeFiles/VerifyFortran.dir/VerifyFortran.f.s

# Object files for target VerifyFortran
VerifyFortran_OBJECTS = \
"CMakeFiles/VerifyFortran.dir/VerifyFortran.f.o"

# External object files for target VerifyFortran
VerifyFortran_EXTERNAL_OBJECTS =

libVerifyFortran.a: CMakeFiles/VerifyFortran.dir/VerifyFortran.f.o
libVerifyFortran.a: CMakeFiles/VerifyFortran.dir/build.make
libVerifyFortran.a: CMakeFiles/VerifyFortran.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking Fortran static library libVerifyFortran.a"
	$(CMAKE_COMMAND) -P CMakeFiles/VerifyFortran.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/VerifyFortran.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/VerifyFortran.dir/build: libVerifyFortran.a
.PHONY : CMakeFiles/VerifyFortran.dir/build

CMakeFiles/VerifyFortran.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/VerifyFortran.dir/cmake_clean.cmake
.PHONY : CMakeFiles/VerifyFortran.dir/clean

CMakeFiles/VerifyFortran.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/Verify /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-pdelab-tutorials/CMakeFiles/FortranCInterface/VerifyCXX/CMakeFiles/VerifyFortran.dir/DependInfo.cmake
.PHONY : CMakeFiles/VerifyFortran.dir/depend

