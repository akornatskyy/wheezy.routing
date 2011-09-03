
""" ``router`` module.
"""

from builders import build_route
from config import route_builders as default_route_builders
from utils import route_name, merge


def url(pattern, handler, kwargs=None, name=None):
    """ Converts parameters to tupple of length four.
        Used for convenience to name parameters and skip
        unused.

        >>> url(r'msg', 'handler', {'id': 1}, name='message')
        ('msg', 'handler', {'id': 1}, 'message')

        Usage:

        >>> class Login: pass
        >>> admin_routes = [
        ...     url(r'login', Login, name='signin')
        ... ]
        >>> r = PathRouter()
        >>> r.add_routes([
        ...     url(r'admin/', admin_routes, kwargs={'site_id': 1})
        ... ])
    """
    return pattern, handler, kwargs, name


class PathRouter(object):
    """
    """

    def __init__(self, route_builders=None):
        """
        """
        self.mapping = []
        self.route_map = {}
        self.routers = []
        self.route_builders = route_builders or \
                default_route_builders

    def add_route(self, pattern, handler,
            kwargs=None, name=None):
        """ Adds a pattern to route table

            >>> r = PathRouter()
            >>> class Login: pass
            >>> r.add_route(r'login', Login)
            >>> assert r.route_map['login']

            You can override the generated name by suppling optional
            ``name`` parameter

            >>> r.add_route(r'login', Login, name='signin')
            >>> assert r.route_map['signin']
            >>> r.path_for('signin')
            'login'
        """
        handler_name = name or route_name(handler)
        route = build_route(pattern, kwargs, self.route_builders)
        self.route_map[handler_name] = route
        self.mapping.append((route, handler))

    def include(self, pattern, included, kwargs=None):
        """ Includes nested routes below the current.

            >>> r = PathRouter()
            >>> class Login: pass
            >>> admin_routes = [
            ...     (r'login', Login)
            ... ]
            >>> r.include(r'admin/', admin_routes)
            >>> route, inner = r.mapping[0]
            >>> inner2, route2 = r.routers[0]
            >>> assert route == route2
            >>> assert inner == inner2
            >>> assert isinstance(inner, PathRouter)
        """
        route = build_route(pattern, kwargs, self.route_builders)
        inner = PathRouter(self.route_builders)
        inner.add_routes(included)
        self.mapping.append((route, inner))
        self.routers.append((inner, route))

    def add_routes(self, mapping):
        """ Adds routes represented as a list of tuple
            (pattern, handler) to route table

            >>> r = PathRouter()
            >>> class Login: pass
            >>> r.add_routes([
            ...     (r'login', Login)
            ... ])
            >>> assert r.mapping
            >>> assert r.route_map

            If ``handler`` is tuple, list or an instance of
            PathRouter than we proceed with ``include`` function

            >>> r = PathRouter()
            >>> class Login: pass
            >>> admin_routes = [(r'login', Login)]
            >>> r.add_routes([
            ...     (r'admin/', admin_routes)
            ... ])
            >>> len(r.routers)
            1
            >>> len(r.mapping)
            1
        """
        for m in mapping:
            l = len(m)
            kwargs, name = None, None
            if l == 2:
                pattern, handler = m
            elif l == 3:
                pattern, handler, kwargs = m
            else:
                pattern, handler, kwargs, name = m

            if isinstance(handler, (tuple, list, PathRouter)):
                self.include(pattern, handler, kwargs)
            else:
                self.add_route(pattern, handler, kwargs, name)

    def match(self, path):
        """ Tries to find a match for the given path in route table.
            Returns a tupple of (handler, kwargs)

            >>> r = PathRouter()
            >>> class Login: pass
            >>> class Message: pass
            >>> r.add_route(r'login', Login)
            >>> handler, kwargs = r.match(r'login')
            >>> assert handler == Login
            >>> kwargs

            Tries to find inner match

            >>> r = PathRouter()
            >>> admin_routes = [
            ...     (r'login', Login
            ... )]
            >>> r.add_routes([
            ...     (r'admin/', admin_routes)
            ... ])
            >>> handler, kwargs = r.match(r'admin/login')
            >>> assert handler == Login

            Merge kwargs

            >>> r = PathRouter()
            >>> admin_routes = [
            ...     (r'msg', Message, {'id': 1})
            ... ]
            >>> r.add_routes([
            ...     (r'en/', admin_routes, {'lang': 'en'})
            ... ])
            >>> handler, kwargs = r.match(r'en/msg')
            >>> assert handler == Message
            >>> kwargs
            {'lang': 'en', 'id': 1}

            Otherwise return (None, None)

            >>> r = PathRouter()
            >>> handler, kwargs = r.match(r'')
            >>> handler
            >>> kwargs
        """
        for route, handler in self.mapping:
            matched, kwargs = route.match(path)
            if matched >= 0:
                # TODO: isinstance(handler, PathRouter)
                handler_match = getattr(handler, 'match', None)
                if not handler_match:
                    return handler, kwargs
                handler, kwargs_inner = handler_match(
                    path[matched:])
                if not kwargs:
                    return handler, kwargs_inner
                if kwargs_inner:
                    kwargs = kwargs.copy()
                    merge(kwargs, kwargs_inner)
                return handler, kwargs
        return None, None

    def path_for(self, name, **kwargs):
        """ Returns the url for the given route name.

            >>> r = PathRouter()
            >>> class Login: pass
            >>> r.add_route(r'login', Login)
            >>> r.path_for(r'login')
            'login'

            Path for inner router

            >>> r = PathRouter()
            >>> admin_routes = [
            ...     (r'login', Login, None, 'signin')
            ... ]
            >>> r.add_routes([
            ...     (r'admin/', admin_routes)
            ... ])
            >>> r.path_for(r'signin')
            'admin/login'

            Otherwise None

            >>> r.path_for(r'unknown')
        """
        route = self.route_map.get(name, None)
        if route:
            return route.path(kwargs)
        for inner, route in self.routers:
            inner_path = inner.path_for(name, **kwargs)
            if inner_path:
                return route.path(kwargs) + inner_path
        return None
