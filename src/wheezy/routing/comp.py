
""" ``p2t3`` module.
"""

import sys


PY3 = sys.version_info[0] >= 3

if PY3:  # pragma: nocover
    basestring = (str, bytes)

    iteritems = lambda d: d.items()

    #import collections
    #callable = lambda obj: isinstance(obj, collections.Callable)
    callable = lambda obj: any("__call__" in klass.__dict__
            for klass in type(obj).__mro__)
else:  # pragma: nocover
    basestring = basestring

    iteritems = lambda d: d.iteritems()

    callable = callable
