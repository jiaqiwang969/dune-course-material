from __future__ import absolute_import

from cgen import *

from dune.codegen.cgen.clazz import Class
from dune.codegen.cgen.exceptions import TryCatchBlock, CatchBlock


class Namespace(PrivateNamespace):
    """
    A namespace Generable that is provided the name of the namespace.
    Normally, you would revert the inheritance here, but I do not want
    to interfere with cgen and for some reason it does not provide
    explicitly named namespace.
    """
    def __init__(self, *args, **kwargs):
        name = kwargs.pop("name")
        PrivateNamespace.__init__(self, *args, **kwargs)

        self.name = name

    def get_namespace_name(self):
        return self.name
