"""
The methods to run the parts of the form compiler

Should also contain the entrypoint methods.
"""
from __future__ import absolute_import


import logging.config

import loopy

from ufl.algorithms import compute_form_data, read_ufl_file
from ufl.algorithms.formfiles import interpret_ufl_namespace

from dune.codegen.generation import (delete_cache_items,
                                     global_context,
                                     )
from dune.codegen.options import (get_driverblock_option,
                                  get_form_option,
                                  get_option,
                                  initialize_options,
                                  )
from dune.codegen.pdelab.driver import (generate_driver,
                                        generate_driver_block,
                                        )
from dune.codegen.pdelab.localoperator import (generate_localoperator_file,
                                               generate_localoperator_kernels,
                                               )
from os.path import splitext, basename, join, dirname, abspath

# Configure loggers
log_file_path = join(dirname(abspath(__file__)), 'logging.conf')
logging.config.fileConfig(log_file_path)

# Disable loopy caching before we do anything else!
loopy.CACHING_ENABLED = False


def type_guessing(val):
    for t in [int, float]:
        try:
            return t(val)
        except ValueError:
            pass
    return val


def read_ufl(uflfile):
    """Read uflfile file, extract and preprocess forms

    Arguments:
    ----------
    uflfile: Path to ufl file.

    Returns:
    --------
    data: The data in the namespace after execution of the UFL file
          and some custom postprocessing.
    """
    # Read the given ufl file and execute it
    uflcode = read_ufl_file(uflfile)

    # Prepopulate a namespace with variation information
    namespace = globals()
    ini = get_option("ini_file")
    if ini:
        from dune.testtools.parametertree.parser import parse_ini_file
        ini = parse_ini_file(ini)

        for k, v in ini.get("formcompiler.ufl_variants", {}).items():
            namespace[k] = type_guessing(v)

    try:
        exec("from dune.codegen.ufl.execution import *\n" + uflcode, namespace)
    except:
        name = splitext(basename(uflfile))[0]
        name = "{}_debug".format(name)
        pyname = "{}.py".format(name)
        print(pyname)
        pycode = "#!/usr/bin/env python\nfrom dune.codegen.ufl.execution import *\nset_level(DEBUG)\n"
        for k, v in ini.get("formcompiler.ufl_variants", {}).items():
            pycode = pycode + "{} = {}\n".format(k, repr(type_guessing(v)))
        pycode = pycode + uflcode
        with open(pyname, "w") as f:
            f.write(pycode)
        raise SyntaxError("Not a valid ufl file, dumped a debug script: {}".format(pyname))

    # Extract and preprocess the forms
    data = interpret_ufl_namespace(namespace)

    # Enrich data by some additional objects to whose name we attached some
    # special meaning.
    if get_option("exact_solution_expression"):
        data.object_by_name[get_option("exact_solution_expression")] = namespace[get_option("exact_solution_expression")]

    magic_names = ("interpolate_expression",
                   "is_dirichlet",
                   "exact_solution",
                   "coarse_space"
                   )
    for name in magic_names:
        data.object_by_name[name] = namespace.get(name, None)

    driverblocks = [i.strip() for i in get_option("driver_blocks").split(",")]
    for db in driverblocks:
        for name in magic_names:
            db_object_name = get_driverblock_option(name, db)
            data.object_by_name[db_object_name] = namespace.get(db_object_name, None)

    return data


def entry_generate_driver():
    """ This is the entry point for driver generation """
    initialize_options()
    data = read_ufl(get_option("uflfile"))

    with global_context(data=data):
        generate_driver()


def entry_generate_driver_block():
    """This is the entry point for driver block generation"""
    initialize_options()
    if get_option("no_driver_block"):
        print("Warning generation of driver block is turned off by the option 'no_driver_block'")
        return
    data = read_ufl(get_option("uflfile"))

    with global_context(data=data):
        driver_block = get_option("driver_block_to_build")

        forms = [i.strip() for i in get_option("operators").split(",")]
        if "mass" in forms:
            forms.remove("mass")
        if get_driverblock_option("spatial_form") is None and len(forms) != 1:
            print("Warning: Can't build driver block. Either specify spatial (and maybe temporal) form in ini file or make sure that you list only one operator (or a second one called mass) in the ini file. If you don't want to build a driver block everything should be fine.")
        else:
            try:
                generate_driver_block(driver_block)
            except:
                raise RuntimeError("Could not build driver block. If you don't want to generate a driver block you can set the option 'no_driver_block = 1' in your ini file.")


def entry_generate_operators():
    """ This is the entry point for operator generation """
    initialize_options()
    data = read_ufl(get_option("uflfile"))

    with global_context(data=data):
        operator = get_option("operator_to_build")
        with global_context(form_identifier=operator):
            # Make sure cache is empty
            delete_cache_items()

            # Choose the form from the UFL input
            kernels = generate_localoperator_kernels(operator)

            # Write the result to a file
            filename = get_form_option("filename")
            generate_localoperator_file(kernels, filename)
