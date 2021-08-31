# Find the actual sources of dune-codegen from downstream modules
# to define dependency on them (otherwise working on the form compiler
# becomes PITA). The cmake variable dune-codegen_DIR only points to the
# *build directory*, the source directory of upstream modules is not
# available through CMake (for good reason).
#
# Do not use this on your own, DuneCodegenMacros.cmake uses this!

import os
import sys
import dune.codegen

path = dune.codegen.__path__[0]
path = os.path.split(os.path.split(path)[0])[0]
sys.stdout.write(path)
sys.exit(0)
