"""
"""

# flake8: noqa: W605

import re

from wheezy.routing.utils import outer_split


def try_build_regex_route(pattern, finishing=True, kwargs=None, name=None):
    """There is no special tests to match regex selection
    strategy.
    """
    if isinstance(pattern, RegexRoute):
        return pattern
    return RegexRoute(pattern, finishing, kwargs, name)


class RegexRoute(object):
    """Route based on regular expression matching."""

    __slots__ = (
        "match",
        "path",
        "path_value",
        "name",
        "path_format",
        "kwargs",
        "regex",
    )

    exact_matches = None

    def __init__(self, pattern, finishing=True, kwargs=None, name=None):
        pattern = pattern.lstrip("^").rstrip("$")
        # Choose match strategy
        self.path_format, names = parse_pattern(pattern)
        if kwargs:
            self.kwargs = dict.fromkeys(names, "")
            self.kwargs.update(kwargs)
            if finishing:
                self.kwargs["route_name"] = name
            self.match = self.match_with_kwargs
            self.path = self.path_with_kwargs
            self.path_value = self.path_format % self.kwargs
        else:
            if finishing:
                self.name = name
                self.match = self.match_no_kwargs_finishing
            else:
                self.match = self.match_no_kwargs
            self.path = self.path_no_kwargs

        pattern = "^" + pattern
        if finishing:
            pattern = pattern + "$"
        self.regex = re.compile(pattern)

    def match_no_kwargs(self, path):
        """If the ``path`` match the regex pattern."""
        m = self.regex.match(path)
        if m:
            return m.end(), m.groupdict()
        return -1, None

    def match_no_kwargs_finishing(self, path):
        """If the ``path`` match the regex pattern."""
        m = self.regex.match(path)
        if m:
            kwargs = m.groupdict()
            kwargs["route_name"] = self.name
            return m.end(), kwargs
        return -1, None

    def match_with_kwargs(self, path):
        """If the ``path`` match the regex pattern."""
        m = self.regex.match(path)
        if m:
            kwargs = m.groupdict()
            return (m.end(), dict(self.kwargs, **kwargs))
        return -1, None

    def path_with_kwargs(self, values=None):
        """Build the path for the given route by substituting
        the named places of the regual expression.

        Specialization case: route was initialized with
        default kwargs.
        """
        if values:
            return self.path_format % dict(self.kwargs, **values)
        else:
            return self.path_value

    def path_no_kwargs(self, values):
        """Build the path for the given route by substituting
        the named places of the regual expression.

        Specialization case: route was initialized with
        no default kwargs.
        """
        return self.path_format % values


RE_SPLIT = re.compile(r"\<(\w+)\>")


def parse_pattern(pattern):
    """Returns path_format and names.

    >>> parse_pattern(r'abc/(?P<id>[^/]+)')
    ('abc/%(id)s', ['id'])
    >>> parse_pattern(r'abc/(?P<n>[^/]+)/(?P<x>\\\w+)')
    ('abc/%(n)s/%(x)s', ['n', 'x'])
    >>> parse_pattern(r'(?P<locale>(en|ru))/home')
    ('%(locale)s/home', ['locale'])

    >>> from wheezy.routing.curly import convert
    >>> parse_pattern(convert(r'[{locale:(en|ru)}/]home'))
    ('%(locale)s/home', ['locale'])
    >>> parse_pattern(convert(r'item[/{id:i}]'))
    ('item/%(id)s', ['id'])

    >>> p = convert('{controller:w}[/{action:w}[/{id:i}]]')
    >>> parse_pattern(p)
    ('%(controller)s/%(action)s/%(id)s', ['controller', 'action', 'id'])
    """
    pattern = strip_optional(pattern)
    parts = outer_split(pattern, sep="()")
    if len(parts) % 2 == 1 and not parts[-1]:
        parts = parts[:-1]
    names = [RE_SPLIT.split(p)[1] for p in parts[1::2]]
    parts[1::2] = ["%%(%s)s" % p for p in names]
    return "".join(parts), names


def strip_optional(pattern):
    """Strip optional regex group flag.

    at the beginning

    >>> strip_optional('((?P<locale>(en|ru))/)?home')
    '(?P<locale>(en|ru))/home'

    at the end

    >>> strip_optional('item(/(?P<id>\\\d+))?')
    'item/(?P<id>\\\d+)'

    nested:

    >>> p = '(?P<controller>\\\w+)(/(?P<action>\\\w+)(/(?P<id>\\\d+))?)?'
    >>> strip_optional(p)
    '(?P<controller>\\\w+)/(?P<action>\\\w+)/(?P<id>\\\d+)'
    """
    if ")?" not in pattern:
        return pattern
    parts = outer_split(pattern, sep="()")
    for i in range(2, len(parts), 2):
        part = parts[i]
        if part.startswith("?"):
            parts[i] = part[1:]
            parts[i - 1] = strip_optional(parts[i - 1])
        else:
            parts[i - 1] = "(%s)" % parts[i - 1]
    return "".join(parts)
