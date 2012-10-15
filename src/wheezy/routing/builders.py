
""" ``builders`` module.
"""

import re

from wheezy.routing.route import PlainRoute
from wheezy.routing.route import RegexRoute
from wheezy.routing.curly import RE_SPLIT as RE_CURLY_ROUTE
from wheezy.routing.curly import convert as curly_convert


RE_PLAIN_ROUTE = re.compile(r'^[\w/-]+$')


def try_build_plain_route(pattern, finishing, kwargs=None, name=None):
    """ If the plain route regular expression match the pattern
        than create a PlainRoute instance.

        >>> pr = PlainRoute(r'abc', True)
        >>> r = try_build_plain_route(pr, True)
        >>> assert pr == r
        >>> r = try_build_plain_route(r'abc', True)
        >>> assert isinstance(r, PlainRoute)

        Otherwise return None.

        >>> r = try_build_plain_route(r'ab[c]', False)
        >>> assert r is None
    """
    if isinstance(pattern, PlainRoute):
        return pattern
    if pattern == '' or RE_PLAIN_ROUTE.match(pattern):
        return PlainRoute(pattern, finishing, kwargs, name)
    return None


def try_build_curly_route(pattern, finishing, kwargs=None, name=None):
    """ Convert pattern expression into regex with
        named groups and create regex route.

        >>> pr = RegexRoute(r'abc', True)
        >>> r = try_build_curly_route(pr, True)
        >>> assert pr == r
        >>> r = try_build_curly_route('abc/{n}', True)
        >>> assert isinstance(r, RegexRoute)

        Otherwise return None.

        >>> r = try_build_curly_route('abc', True)
    """
    if isinstance(pattern, RegexRoute):
        return pattern
    if RE_CURLY_ROUTE.search(pattern):
        return RegexRoute(curly_convert(pattern), finishing, kwargs, name)
    return None


def try_build_regex_route(pattern, finishing, kwargs=None, name=None):
    """ There is no special tests to match regex selection
        strategy.

        >>> pr = RegexRoute(r'abc', True)
        >>> r = try_build_regex_route(pr, True)
        >>> assert pr == r
        >>> r = try_build_regex_route(r'abc', True)
        >>> assert isinstance(r, RegexRoute)
    """
    if isinstance(pattern, RegexRoute):
        return pattern
    return RegexRoute(pattern, finishing, kwargs, name)


def build_route(pattern, finishing, kwargs, name, route_builders):
    """ Try to find suitable route builder to create a route.

        >>> from wheezy.routing.config import route_builders
        >>> r = build_route(r'abc', False, {'a': 1}, None, route_builders)
        >>> assert isinstance(r, PlainRoute)
        >>> r.kwargs
        {'a': 1}

        Otherwise raise LookupError

        >>> r = build_route(r'abc', None, False, None, [])
        Traceback (most recent call last):
            ...
        LookupError: No matching route factory found
    """
    if not finishing:
        assert not name
    for try_build_route in route_builders:
        route = try_build_route(pattern, finishing, kwargs, name)
        if route:
            return route
    else:
        raise LookupError("No matching route factory found")
