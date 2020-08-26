""" ``route`` module.
"""


class Route(object):
    """Route abstract contract."""

    exact_matches = None

    def match(self, path):
        """if the ``path`` matches, return the end of
        substring matched and kwargs. Otherwise
        return ``(-1, None)``.
        """
        raise NotImplementedError()

    def path(self, values=None):
        """Build the path for given route."""
        raise NotImplementedError()
