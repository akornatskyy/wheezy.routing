""" ``plain`` module.
"""

import re

RE_PLAIN_ROUTE = re.compile(r"^[\w\./-]+$")


def try_build_plain_route(pattern, finishing=True, kwargs=None, name=None):
    """If the plain route regular expression match the pattern
    than create a PlainRoute instance.
    """
    if isinstance(pattern, PlainRoute):
        return pattern
    if pattern == "" or RE_PLAIN_ROUTE.match(pattern):
        return PlainRoute(pattern, finishing, kwargs, name)
    return None


class PlainRoute(object):
    """Route based on string equalty operation."""

    __slots__ = ("pattern", "kwargs", "matched", "match", "exact_matches")

    def __init__(self, pattern, finishing, kwargs=None, name=None):
        """Initializes the route by given ``pattern``. If
        ``finishing`` is True than choose ``equals_math``
        strategy
        """
        kwargs = kwargs and kwargs.copy() or {}
        self.pattern = pattern
        self.matched = len(pattern)
        # Choose match strategy
        if finishing:
            if name:
                kwargs["route_name"] = name
            self.match = self.equals_match
        else:
            self.match = self.startswith_match
        self.exact_matches = ((pattern, kwargs),)
        self.kwargs = kwargs

    def equals_match(self, path):
        """If the ``path`` exactly equals pattern string,
        return end index of substring matched and a copy
        of ``self.kwargs``.
        """
        return (
            path == self.pattern and (self.matched, self.kwargs) or (-1, None)
        )

    def startswith_match(self, path):
        """If the ``path`` starts with pattern string, return
        the end of substring matched and ``self.kwargs``.
        """
        return (
            path.startswith(self.pattern)
            and (self.matched, self.kwargs)
            or (-1, None)
        )

    def path(self, values=None):
        """Build the path for given route by simply returning
        the pattern used during initialization.
        """
        return self.pattern
