""" ``plain`` module.
"""

import re

RE_CHOICE_ROUTE = re.compile(
    r"^(?P<p>[\w/]*)" r"\{(?P<n>\w+):\((?P<c>[\w|]+)\)\}" r"(?P<s>[\w/]*)$"
)


def try_build_choice_route(pattern, finishing=True, kwargs=None, name=None):
    """If the choince route regular expression match the pattern
    than create a ChoiceRoute instance.
    """
    if isinstance(pattern, ChoiceRoute):
        return pattern
    m = RE_CHOICE_ROUTE.match(pattern)
    if m:
        return ChoiceRoute(pattern, finishing, kwargs, name)
    return None


class ChoiceRoute(object):
    """Route based on choice match, e.g. {locale:(en|ru)}."""

    __slots__ = ("kwargs", "name", "exact_matches", "patterns", "path_format")

    def __init__(self, pattern, finishing=True, kwargs=None, name=None):
        kwargs = kwargs and kwargs.copy() or {}
        if name:
            kwargs["route_name"] = name
        self.kwargs = kwargs
        m = RE_CHOICE_ROUTE.match(pattern)
        prefix, self.name, choice, suffix = m.groups()
        choices = choice.split("|")
        self.exact_matches = [
            (prefix + c + suffix, dict(kwargs, **{self.name: c}))
            for c in choices
        ]
        self.patterns = [(p, (len(p), kw)) for p, kw in self.exact_matches]
        self.path_format = prefix + "%s" + suffix

    def match(self, path):
        """If the ``path`` matches, return the end of
        substring matched and kwargs. Otherwise
        return ``(-1, None)``.
        """
        for pattern, result in self.patterns:
            if path.startswith(pattern):
                return result
        return (-1, None)

    def path(self, values=None):
        """Build the path for given route."""
        if not values or self.name not in values:
            values = self.kwargs
        return self.path_format % values[self.name]
