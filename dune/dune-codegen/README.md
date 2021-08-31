# dune-codegen

dune-codegen is an active research project with the goal of
generating high-performance integration kernels for the Dune project.

It currently provides the following features:
* Robust generation of integration kernels from the Unified Form Language (UFL) for use with dune-pdelab.
* Integration of a code generation workflow into the Dune CMake build system
* Code generation of DG methods exploiting finite element tensor product structure (sum factorization)
* Code generation for block-structured FEM

[![pipeline status](https://gitlab.dune-project.org/extensions/dune-codegen/badges/master/pipeline.svg)](https://gitlab.dune-project.org/extensions/dune-codegen/commits/master)


## Dependencies

dune-codegen currently depends on the following software packages:

* You need a working [dune-pdelab][1].

* We use [dune-testtools][2] for ini file variablility.

* The [Integer Set Library][3] needs to be installed. Using the
  package manager is probably the easiest way.


## Cloning and Patching

We use several submodules so you should clone with the `--recursive` option:

```
git clone --recursive ssh://git@gitlab.dune-project.org:22022/extensions/dune-codegen.git
```

or

```
git clone --recursive https://gitlab.dune-project.org/extensions/dune-codegen.git
```

If you have a feature branch `feature/my-branch` where you change the
submodules of dune-codegen and you want to test your branch it makes
sense to checkout this branch directly in a fresh clone:

```
git clone --recursive -b feature/my-branch ssh://git@gitlab.dune-project.org:22022/dominic/dune-codegen.git
```

Some tests compare the vtkoutput to a reference vtk output. If you
want to have all tests passing you need to install [git-lfs][0] before
cloning. Cloning via ssh and using a ssh-agent are recommended in this
case:

```
ssh-add
git clone --recursive ssh://git@gitlab.dune-project.org:22022/dominic/dune-codegen.git
```

After cloning dune-codegen you need apply some patches:

* Go to the base folder of dune-codegen and run
  patches/apply_patches.sh. This applies patches to the submodules.

  ```
  cd dune-codegen/
  ./patches/apply_patches.sh
  ```

## Building dune-codegen

Building dune-codegen is done through the Dune build-system using
cmake. See the [Dune homepage][4] for further details. You need to set the options

```
-DDUNE_PYTHON_ALLOW_GET_PIP=1
-DDUNE_PYTHON_VIRTUALENV_SETUP=1
```

in your options file. Your options file could for example look like
the following:

```
CMAKE_FLAGS="
  -DDUNE_PYTHON_FORCE_PYTHON3=1
  -DDUNE_PYTHON_ALLOW_GET_PIP=1
  -DDUNE_PYTHON_VIRTUALENV_SETUP=1
  -DCMAKE_BUILD_TYPE=Release
  -DCMAKE_CXX_FLAGS='-march=native -ffast-math'
  -DDUNE_SYMLINK_TO_SOURCE_TREE=1
"

MAKE_FLAGS="-j2"
```


## Building and Running the Tests

You can build and run the tests via:

```
cd path/to/dune-codegen/build/directory
make build_tests
ctest
```

Note that this takes quite a while.

## Building and Running dune-codegen in an offline environment

dune-codegen relies on installing Python packages into self-contained environments
during its configuration and build process. In order to do this in an offline
environment, we recommend using the tool `devpi`. One of its use cases is to provide
a local mirror for the Python package index. A quickstart tutorial for this use case
is available [5]. It boils down to the following:

* Installing the `devpi-server` package through your favorite method
* Setting up a local server with `devpi-server --init`
* Making sure it is running in the background (explicitly with `devpi-server --start/stop` or by configuring a systemd service.
* Have the environment variable `PIP_INDEX_URL` to its index, e.g. by adding this line to your `~/.bashrc` (where `http://localhost:3141` might differ depending on your devpi configuration):
```
export PIP_INDEX_URL=http://localhost:3141/root/pypi/+simple/
```

At first installation, the locally mirrored package index will access PyPI.
Later on, it will install packages from its local cache.

## Links

[0]: https://git-lfs.github.com/
[1]: https://gitlab.dune-project.org/pdelab/dune-pdelab
[2]: https://gitlab.dune-project.org/quality/dune-testtools
[3]: http://isl.gforge.inria.fr/
[4]: https://www.dune-project.org/doc/installation/
[5]: https://github.com/devpi/devpi/blob/master/doc/quickstart-pypimirror.rst
