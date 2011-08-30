import re

from route import Route
from route import PlainRoute


PLAIN_ROUTE_REGEX = re.compile('^[\w/-]+$')


def try_build_plain_route(pattern, kwargs=None):
    """ If the plain route regular expression match the pattern
        than create a PlainRoute instance.

        ``equals_match`` strategy:

        >>> r = try_build_plain_route(r'abc')
        >>> assert isinstance(r, PlainRoute)
        >>> assert r.match == r.equals_match

        ``startswith_match`` strategy:

        >>> r = try_build_plain_route(r'abc/')
        >>> assert isinstance(r, PlainRoute)
        >>> assert r.match == r.startswith_match

        Otherwise return None.

        >>> r = try_build_plain_route(r'ab[c]')
        >>> assert r is None
    """
    if PLAIN_ROUTE_REGEX.match(pattern):
        return PlainRoute(pattern, kwargs, equals=pattern[-1:] != '/')
    return None

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


