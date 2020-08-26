""" ``builders`` module.
"""


def build_route(pattern, finishing, kwargs, name, route_builders):
    """Try to find suitable route builder to create a route.
    Raises ``LookupError`` if none found.
    """
    if not finishing:
        assert not name
    for try_build_route in route_builders:
        route = try_build_route(pattern, finishing, kwargs, name)
        if route:
            return route
    else:
        raise LookupError("No matching route factory found")
