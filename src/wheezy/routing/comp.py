
""" ``comp`` module.
"""

import sys


PY3 = sys.version_info[0] >= 3

if PY3:  # pragma: nocover
    basestring = (str, bytes)

    def ntob(n, encoding):
        """ Converts native string to bytes
        """
        return n.encode(encoding)

    #import collections
    #callable = lambda obj: isinstance(obj, collections.Callable)
    callable = lambda obj: any(
        "__call__" in klass.__dict__ for klass in type(obj).__mro__)
else:  # pragma: nocover
    basestring = basestring

    def ntob(n, encoding):
        """ Converts native string to bytes
        """
        return n

    callable = callable


if PY3:  # pragma: nocover
    iteritems = lambda d: d.items()
    copyitems = lambda d: list(d.items())
else:  # pragma: nocover
    iteritems = lambda d: d.iteritems()
    copyitems = lambda d: d.items()
