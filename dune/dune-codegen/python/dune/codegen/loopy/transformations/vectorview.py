"""
Implement tools around the idea of having two 'views' on memory:
One being an ordinary array with proper shape and so on, and one
being a an array of SIMD vectors
"""

from dune.codegen.loopy.target import dtype_floatingpoint
from dune.codegen.loopy.temporary import DuneTemporaryVariable
from dune.codegen.loopy.vcl import get_vcl_type_size
from dune.codegen.tools import round_to_multiple

import loopy as lp
import numpy as np
import pymbolic.primitives as prim
import pytools as pt


def get_vector_view_name(tmpname):
    return tmpname + "_vec"


def add_vector_view(knl, tmpname, pad_to=1):
    temporaries = knl.temporary_variables
    temp = temporaries[tmpname]
    vectemp = get_vector_view_name(tmpname)
    bsname = tmpname + "_base"
    vecsize = get_vcl_type_size(temp.dtype)

    # Enforce idempotency
    if vectemp in temporaries:
        return knl

    # Modify the original temporary to use our custom base storage mechanism
    if isinstance(temp, DuneTemporaryVariable):
        if temp.custom_base_storage:
            bsname = temp.custom_base_storage
        else:
            temp = temp.copy(custom_base_storage=bsname)
            temporaries[tmpname] = temp
    else:
        temp = DuneTemporaryVariable(custom_base_storage=bsname,
                                     managed=True,
                                     **temp.get_copy_kwargs()
                                     )
        temporaries[tmpname] = temp

    size = round_to_multiple(pt.product(temp.shape), vecsize) // vecsize
    size = round_to_multiple(size, pad_to)

    # Now add a vector view temporary
    temporaries[vectemp] = DuneTemporaryVariable(vectemp,
                                                 dim_tags="c,vec",
                                                 shape=(size, vecsize),
                                                 custom_base_storage=bsname,
                                                 scope=lp.temp_var_scope.PRIVATE,
                                                 managed=True,
                                                 )

    # Avoid that these temporaries are eliminated
    silenced = ['temp_to_write({})'.format(vectemp),
                'read_no_write({})'.format(vectemp),
                ]

    return knl.copy(temporary_variables=temporaries,
                    silenced_warnings=knl.silenced_warnings + silenced)
