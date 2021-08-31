# Return the list of generated files for a given ini file
# This is used by the build system, do not use this yourself!

from dune.testtools.parser import parse_ini_file
from dune.testtools.cmakeoutput import printForCMake

import sys

ini = parse_ini_file(sys.argv[1])
section = ini.get("formcompiler", {})
operators = section.get("operators", "r")
operators = [i.strip() for i in operators.split(",")]
driver_blocks = section.get("driver_blocks", "default_driver_block")
driver_blocks = [i.strip() for i in driver_blocks.split(",")]


def get_filename(operator):
    ssection = ini.get("formcompiler.{}".format(operator), {})
    if ssection.get("filename", None):
        return ssection["filename"]
    else:
        classname = ssection.get("classname", "{}Operator".format(ssection.get("form", operator)))
        return "{}_{}_db.hh".format(sys.argv[2], classname)


def driver_block_filename(db):
    ssection = ini.get("formcompiler.driverblock.{}".format(db), {})
    if ssection.get("filename", None):
        return ssection["filename"]
    else:
        classname = ssection.get("classname", "DriverBlock")
        return "{}_{}_file.hh".format(sys.argv[2], classname.lower())


result = {"__{}".format(o): get_filename(o) for o in operators}
result.update({"__db{}".format(db): driver_block_filename(db) for db in driver_blocks})
result["__operators"] = ";".join(operators)
result["__driverblocks"] = ";".join(driver_blocks)

printForCMake(result, sys.argv[3])
sys.exit(0)
