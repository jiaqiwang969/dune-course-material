""" All the infrastructure code related to adding hooks to the code generation process """


_hooks = {}


def hook(hookname):
    """ A decorator for hook functions """

    def _hook(func):
        current = _hooks.setdefault(hookname, ())
        current = list(current)
        current.append(func)
        _hooks[hookname] = tuple(current)

        return func

    return _hook


class ReturnArg(object):
    """ A wrapper for a hook argument, that will be replaced with
    the return value of the previous hook functions. That allows
    a chain of function calls like a loopy transformation sequence.
    """
    def __init__(self, arg):
        self.arg = arg


def run_hook(name=None, args=[], kwargs={}):
    if name is None:
        raise CodegenError("Running hook requires the hook name!")

    # Handle occurences of ReturnArg in the given arguments
    occ = list(isinstance(a, ReturnArg) for a in args)
    assert occ.count(True) <= 1
    index = None
    if occ.count(True):
        index = occ.index(True)
    args = list(args)
    ret = None
    if index is not None:
        ret = args[index].arg

    # Run the actual hooks
    for hook in _hooks.get(name, ()):
        # Modify the args for chained hooks
        if index is not None:
            args[index] = ret

        ret = hook(*args, **kwargs)

    return ret
