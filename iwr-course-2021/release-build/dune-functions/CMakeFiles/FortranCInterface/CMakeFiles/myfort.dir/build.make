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
CMAKE_SOURCE_DIR = /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface

# Include any dependencies generated for this target.
include CMakeFiles/myfort.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include CMakeFiles/myfort.dir/compiler_depend.make

# Include the progress variables for this target.
include CMakeFiles/myfort.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/myfort.dir/flags.make

CMakeFiles/myfort.dir/mysub.f.o: CMakeFiles/myfort.dir/flags.make
CMakeFiles/myfort.dir/mysub.f.o: /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mysub.f
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building Fortran object CMakeFiles/myfort.dir/mysub.f.o"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -c /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mysub.f -o CMakeFiles/myfort.dir/mysub.f.o

CMakeFiles/myfort.dir/mysub.f.i: cmake_force
	@echo "Preprocessing Fortran source to CMakeFiles/myfort.dir/mysub.f.i"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -E /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mysub.f > CMakeFiles/myfort.dir/mysub.f.i

CMakeFiles/myfort.dir/mysub.f.s: cmake_force
	@echo "Compiling Fortran source to assembly CMakeFiles/myfort.dir/mysub.f.s"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -S /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mysub.f -o CMakeFiles/myfort.dir/mysub.f.s

CMakeFiles/myfort.dir/my_sub.f.o: CMakeFiles/myfort.dir/flags.make
CMakeFiles/myfort.dir/my_sub.f.o: /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_sub.f
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Building Fortran object CMakeFiles/myfort.dir/my_sub.f.o"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -c /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_sub.f -o CMakeFiles/myfort.dir/my_sub.f.o

CMakeFiles/myfort.dir/my_sub.f.i: cmake_force
	@echo "Preprocessing Fortran source to CMakeFiles/myfort.dir/my_sub.f.i"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -E /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_sub.f > CMakeFiles/myfort.dir/my_sub.f.i

CMakeFiles/myfort.dir/my_sub.f.s: cmake_force
	@echo "Compiling Fortran source to assembly CMakeFiles/myfort.dir/my_sub.f.s"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -S /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_sub.f -o CMakeFiles/myfort.dir/my_sub.f.s

CMakeFiles/myfort.dir/mymodule.f90.o: CMakeFiles/myfort.dir/flags.make
CMakeFiles/myfort.dir/mymodule.f90.o: /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mymodule.f90
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface/CMakeFiles --progress-num=$(CMAKE_PROGRESS_3) "Building Fortran object CMakeFiles/myfort.dir/mymodule.f90.o"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -c /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mymodule.f90 -o CMakeFiles/myfort.dir/mymodule.f90.o

CMakeFiles/myfort.dir/mymodule.f90.i: cmake_force
	@echo "Preprocessing Fortran source to CMakeFiles/myfort.dir/mymodule.f90.i"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -E /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mymodule.f90 > CMakeFiles/myfort.dir/mymodule.f90.i

CMakeFiles/myfort.dir/mymodule.f90.s: cmake_force
	@echo "Compiling Fortran source to assembly CMakeFiles/myfort.dir/mymodule.f90.s"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -S /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/mymodule.f90 -o CMakeFiles/myfort.dir/mymodule.f90.s

CMakeFiles/myfort.dir/my_module.f90.o: CMakeFiles/myfort.dir/flags.make
CMakeFiles/myfort.dir/my_module.f90.o: /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_module.f90
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface/CMakeFiles --progress-num=$(CMAKE_PROGRESS_4) "Building Fortran object CMakeFiles/myfort.dir/my_module.f90.o"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -c /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_module.f90 -o CMakeFiles/myfort.dir/my_module.f90.o

CMakeFiles/myfort.dir/my_module.f90.i: cmake_force
	@echo "Preprocessing Fortran source to CMakeFiles/myfort.dir/my_module.f90.i"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -E /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_module.f90 > CMakeFiles/myfort.dir/my_module.f90.i

CMakeFiles/myfort.dir/my_module.f90.s: cmake_force
	@echo "Compiling Fortran source to assembly CMakeFiles/myfort.dir/my_module.f90.s"
	/opt/homebrew/bin/gfortran $(Fortran_DEFINES) $(Fortran_INCLUDES) $(Fortran_FLAGS) -S /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface/my_module.f90 -o CMakeFiles/myfort.dir/my_module.f90.s

# Object files for target myfort
myfort_OBJECTS = \
"CMakeFiles/myfort.dir/mysub.f.o" \
"CMakeFiles/myfort.dir/my_sub.f.o" \
"CMakeFiles/myfort.dir/mymodule.f90.o" \
"CMakeFiles/myfort.dir/my_module.f90.o"

# External object files for target myfort
myfort_EXTERNAL_OBJECTS =

libmyfort.a: CMakeFiles/myfort.dir/mysub.f.o
libmyfort.a: CMakeFiles/myfort.dir/my_sub.f.o
libmyfort.a: CMakeFiles/myfort.dir/mymodule.f90.o
libmyfort.a: CMakeFiles/myfort.dir/my_module.f90.o
libmyfort.a: CMakeFiles/myfort.dir/build.make
libmyfort.a: CMakeFiles/myfort.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --progress-dir=/Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface/CMakeFiles --progress-num=$(CMAKE_PROGRESS_5) "Linking Fortran static library libmyfort.a"
	$(CMAKE_COMMAND) -P CMakeFiles/myfort.dir/cmake_clean_target.cmake
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/myfort.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/myfort.dir/build: libmyfort.a
.PHONY : CMakeFiles/myfort.dir/build

CMakeFiles/myfort.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/myfort.dir/cmake_clean.cmake
.PHONY : CMakeFiles/myfort.dir/clean

CMakeFiles/myfort.dir/depend:
	cd /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface /opt/homebrew/Cellar/cmake/3.20.4/share/cmake/Modules/FortranCInterface /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface /Users/wjq/Documents/Github-CI/deal.II-mini/temp/iwr-course-2021/release-build/dune-functions/CMakeFiles/FortranCInterface/CMakeFiles/myfort.dir/DependInfo.cmake
.PHONY : CMakeFiles/myfort.dir/depend
