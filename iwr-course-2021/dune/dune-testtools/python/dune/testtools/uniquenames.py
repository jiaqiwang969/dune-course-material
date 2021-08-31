""" A module to make values in dicts unique within a list of dicts.

.. currentmodule:: dune.testtools.uniquenames

Unique names are needed to implement naming schemes of ini files
and static configurations alike. There,
a naming scheme might be given, but it may not be unique.

Commands
++++++++

.. _unique:
.. metaini_command:: unique

    The ``unique`` command can be applied to any value that has to
    be unique within the whole set of generated ini files. It is usefule
    to provide e.g. unique names for output files to be generated by tests,
    as the tests would otherwise overwrite output of other tests.

    The special ``__name`` key in meta ini files has the ``unique`` command
    applied automatically to ensure unique names for the ini files themselves.

    .. note::
        Other keys cannot depend on keys that have to
        ``unique`` command applied, as uniqueness is taken care of
        after the expansion process. ``dune-testtools`` will throw
        a ``ValueError`` if you try to.

"""
from __future__ import absolute_import
from dune.testtools.command import meta_ini_command, CommandType


@meta_ini_command(name="unique", ctype=CommandType.POST_FILTERING, returnValue=False)
def make_key_unique(configs=None, key=None):
    """Defines the meta ini command ``unique``"""
    # first count the number of occurences of the values
    key_dict = {}
    for c in configs:
        # If the key isnt even in the dict, add it as "" to allow a numbered scheme
        if key not in c:
            c[key] = ""
        if c[key] not in key_dict:
            key_dict[c[key]] = 1
        else:
            key_dict[c[key]] += 1

    # Now delete all those that appeared only once (those are unique already) and reset all the others to 0
    for k, count in list(key_dict.items()):
        if count is 1:
            del key_dict[k]
        else:
            key_dict[k] = 0

    # Now make the values unique
    for c in configs:
        # Check whether this value was found multiple times. If so, it has to be made unique.
        if c[key] in key_dict:
            # increase the counter in key_dict for the given key
            key_dict[c[key]] += 1

            # check whether we have numbering only (doesnt need an underscore)
            if c[key] == "":
                c[key] = str(key_dict[""] - 1).zfill(4)
            else:
                c[key] = c[key] + "_" + str(key_dict[c[key]] - 1).zfill(4)