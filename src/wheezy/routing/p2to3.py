
""" ``p2t3`` module.
"""

import sys


PY3 = sys.version_info[0] == 3

if PY3:  # pragma: nocover
    import collections
    string_type = str

    def iscallable(obj):
        #return isinstance(obj, collections.Callable)
        return any("__call__" in klass.__dict__
            for klass in type(obj).__mro__)
else:  # pragma: nocover
    string_type = basestring
    iscallable = callable
