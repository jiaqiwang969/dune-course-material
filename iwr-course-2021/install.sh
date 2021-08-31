#!/bin/bash


# This script is part of the convenience build system for the IWR Dune course.
# It installs all the dune modules used throughout the course.
#
# The following environment variables are recognized:
# F77 the fortran compiler (gfortran)
# CC the C compiler (gcc)
# CXX the C++ compiler (g++)
# CXXFLAGS the standard C++ flags for external libraries ("-O3 -DNEBUG")
# CFLAGS the standard C flags for external libraries (copy CXXFLAGS)
# MAKE_FLAGS flags to be given to make during the build process ("-j2")

ROOT=$(pwd)
if [ ! "$F77" ]; then
  F77=gfortran
fi
if [ ! "$CC" ]; then
CC=gcc
fi
if [ ! "$CXX" ]; then
CXX=g++
fi
if [ ! "$CXXFLAGS" ]; then
CXXFLAGS="-O3 -DNDEBUG"
fi
CFLAGS="$CXXFLAGS"
if [ ! "$MAKE_FLAGS" ]; then
MAKE_FLAGS="-j20"
fi

# To avoid an ugly cmake bug we expand our compiler variables to absolute paths
export CC=$(which $CC)
export CXX=$(which $CXX)
export F77=$(which $F77)

# Initialize submodules
git submodule update --init --recursive

# The code generation module needs to apply patches before building
pushd dune/dune-codegen/
./patches/apply_patches.sh
popd

# generate an opts file with releases flags
echo "CMAKE_FLAGS=\"
-DCMAKE_C_COMPILER='$CC'
-DCMAKE_CXX_COMPILER='$CXX'
-DCMAKE_CXX_FLAGS='-Wall -DDUNE_AVOID_CAPABILITIES_IS_PARALLEL_DEPRECATION_WARNING'
-DDUNE_PYTHON_ALLOW_GET_PIP=1
-DDUNE_PYTHON_VIRTUALENV_SETUP=1
-DCMAKE_CXX_FLAGS_RELEASE='-O3 -DNDEBUG -g0 -funroll-loops'
-DDUNE_SYMLINK_TO_SOURCE_TREE=1
-DCMAKE_BUILD_TYPE=Release
\"" > release.opts

# generate an opts file with debug flags
echo "CMAKE_FLAGS=\"
-DCMAKE_C_COMPILER='$CC'
-DCMAKE_CXX_COMPILER='$CXX'
-DDUNE_PYTHON_ALLOW_GET_PIP=1
-DDUNE_PYTHON_VIRTUALENV_SETUP=1
-DCMAKE_CXX_FLAGS='-Wall -DDUNE_AVOID_CAPABILITIES_IS_PARALLEL_DEPRECATION_WARNING'
-DCMAKE_CXX_FLAGS_DEBUG='-O0 -ggdb'
-DDUNE_SYMLINK_TO_SOURCE_TREE=1
-DCMAKE_BUILD_TYPE=Debug
\"" > debug.opts

rm -rf debug-build release-build

./dune/dune-common/bin/dunecontrol --opts=release.opts --builddir=$(pwd)/release-build --module=dune-pdelab-tutorials all

# You could create a debug build this way:
# ./dune/dune-common/bin/dunecontrol --opts=debug.opts --builddir=$(pwd)/debug-build --module=dune-pdelab-tutorials all

