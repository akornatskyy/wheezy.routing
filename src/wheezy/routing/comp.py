
""" ``p2t3`` module.
"""

import sys


PY3 = sys.version_info[0] == 3

if PY3:  # pragma: nocover
    import collections
    string_type = str

    iteritems = lambda d: d.items()

    #lambda obj: isinstance(obj, collections.Callable)
    lambda obj: any("__call__" in klass.__dict__
            for klass in type(obj).__mro__)
else:  # pragma: nocover
    string_type = basestring

    iteritems = lambda d: d.iteritems()

    iscallable = callable
