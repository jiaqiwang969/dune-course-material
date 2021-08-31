# Disallow numpy to use multithreading - it breaks parallel code generation
# on machines with large core count.
import os
os.environ["OMP_NUM_THREADS"] = "1"

# Trigger imports that involve monkey patching!
import dune.codegen.loopy.symbolic  # noqa

# Trigger some imports that are needed to have all mixin implementations visible
import dune.codegen.pdelab  # noqa
import dune.codegen.sumfact  # noqa
import dune.codegen.blockstructured  # noqa

# Trigger imports that register finite elements in UFL
import dune.codegen.ufl.finiteelement  # noqa
