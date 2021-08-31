#!/usr/bin/env python

import time
import sys
import subprocess
import os

os.environ['DUNE_CODEGEN_THREADS'] = '20'

# Run the actual command

# The actual measurements will be called like this (mpi parallelism)
# command = "srun -p haswell10c -n 20 -c 2 --cpu_bin=verbose,core".split()

# Command for autotune benchmarks with threading
command = "srun -p haswell10c -n 1 -c 20 --hint=nomultithread --cpu_bin=verbose,core".split()

command.extend(sys.argv[1:])
ret = subprocess.call(command)

# If that failed - fail!
if ret != 0:
    sys.exit(ret)
