""" Some global counters used to generate unique names throughout the project """

_counts = {}


def get_counter(identifier):
    count = _counts.setdefault(identifier, 0)
    _counts[identifier] = _counts[identifier] + 1
    return count


def get_counted_variable(identifier):
    ret = "{}_{}".format(identifier, str(get_counter(identifier)).zfill(4))
    return ret
