import re

from route import Route
from route import PlainRoute
from route import RegexRoute


RE_PLAIN_ROUTE = re.compile('^[\w/-]+$')


def try_build_plain_route(pattern, kwargs=None):
    """ If the plain route regular expression match the pattern
        than create a PlainRoute instance.

        >>> r = try_build_plain_route(r'abc')
        >>> assert isinstance(r, PlainRoute)

        Otherwise return None.

        >>> r = try_build_plain_route(r'ab[c]')
        >>> assert r is None
    """
    if pattern == '' or RE_PLAIN_ROUTE.match(pattern):
        return PlainRoute(pattern, kwargs)
    return None


def try_build_regex_route(pattern, kwargs=None):
    """ There is no special tests to match regex selection
        strategy.

        >>> r = try_build_regex_route(r'abc')
        >>> assert isinstance(r, RegexRoute)
    """
    return RegexRoute(pattern, kwargs)


def build_route(pattern, kwargs, route_builders):
    """ If ``pattern`` is an object drived from ``Route`` than it
        simply returned.

        >>> pattern = PlainRoute(r'abc')
        >>> r = build_route(pattern, None, [])
        >>> assert pattern == r

        If ``pattern`` is a string than try to find
        sutable route builder to create a route.

        >>> from config import route_builders
        >>> r = build_route(r'abc', {'a': 1}, route_builders)
        >>> assert isinstance(r, PlainRoute)
        >>> r.kwargs
        {'a': 1}

        Otherwise raise LookupError

        >>> r = build_route(r'abc', None, [])
        Traceback (most recent call last):
            ...
        LookupError: No matching route factory found
    """
    if isinstance(pattern, Route):
        route = pattern
    else:
        for try_build_route in route_builders:
            route = try_build_route(pattern, kwargs)
            if route:
                break
        else:
            raise LookupError("No matching route factory found")
    return route
