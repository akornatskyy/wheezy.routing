
""" ``router`` module.
"""

from warnings import warn

from wheezy.routing.builders import build_route
from wheezy.routing.config import route_builders as default_route_builders
from wheezy.routing.utils import merge
from wheezy.routing.utils import route_name


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
    __slots__ = ('mapping', 'path_map', 'route_map', 'inner_route_map',
                 'route_builders')

    def __init__(self, route_builders=None):
        """
        """
        self.mapping = []
        self.route_map = {}
        self.path_map = {}
        self.inner_route_map = {}
        self.route_builders = route_builders or default_route_builders

    def add_route(self, pattern, handler, kwargs=None, name=None):
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

            If ``name`` already mapped to some route allow
            override it but show a warning.

            >>> import warnings
            >>> warnings.simplefilter('ignore')
            >>> def login_handler(): pass
            >>> r.add_route(r'test', login_handler, name='signin')
            >>> warnings.simplefilter('default')
            >>> r.path_for('signin')
            'test'
        """
        name = name or route_name(handler)
        if name in self.route_map:
            warn('PathRouter: overriding route: %s.' % name)
        kwargs = kwargs or {}
        kwargs['route_name'] = name
        # build finishing route
        route = build_route(pattern, True, kwargs, self.route_builders)
        self.route_map[name] = route.path
        if hasattr(route, 'exact_matches'):
            for pattern, kwargs in route.exact_matches:
                if pattern in self.path_map:
                    warn('PathRouter: overriding path: %s.' % pattern)
                self.path_map[pattern] = (handler, kwargs)
        else:
            self.mapping.append((route.match, handler))

    def include(self, pattern, included, kwargs=None):
        """ Includes nested routes below the current.

            >>> r = PathRouter()
            >>> class Login: pass
            >>> admin_routes = [
            ...     (r'login', Login)
            ... ]
            >>> r.include(r'admin/', admin_routes)
            >>> route, inner = r.mapping[0]
            >>> assert isinstance(inner, PathRouter)
            >>> r = PathRouter()
            >>> inner = PathRouter()
            >>> inner.add_routes([(r'login', Login)])
            >>> r.include(r'admin/', inner)
            >>> assert r.inner_route_map

            If ``name`` already mapped to some route allow
            override it but show a warning.

            >>> import warnings
            >>> warnings.simplefilter('ignore')
            >>> r.include(r'admin/', admin_routes)
            >>> top_router = PathRouter()
            >>> r.include(r'x/', r)
            >>> warnings.simplefilter('default')
        """
        # try build intermediate route
        route = build_route(pattern, False, kwargs, self.route_builders)
        if isinstance(included, PathRouter):
            inner = included
        else:
            inner = PathRouter(self.route_builders)
            inner.add_routes(included)
        self.mapping.append((route.match, inner))
        route_path = route.path
        for name, path in inner.route_map.items():
            if name in self.inner_route_map:
                warn('PathRouter: overriding route: %s.' % name)
            self.inner_route_map[name] = [route_path, path]
        for name, paths in inner.inner_route_map.items():
            if name in self.inner_route_map:
                warn('PathRouter: overriding route: %s.' % name)
            self.inner_route_map[name] = [route_path] + paths

    def add_routes(self, mapping):
        """ Adds routes represented as a list of tuple
            (pattern, handler) to route table

            >>> r = PathRouter()
            >>> class Login: pass
            >>> r.add_routes([
            ...     (r'login', Login)
            ... ])

            >> assert r.mapping
            >> assert r.route_map

            If ``handler`` is tuple, list or an instance of
            PathRouter than we proceed with ``include`` function

            >>> r = PathRouter()
            >>> class Login: pass
            >>> admin_routes = [(r'login', Login)]
            >>> r.add_routes([
            ...     (r'admin/', admin_routes)
            ... ])
            >>> len(r.inner_route_map)
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
            {'route_name': 'login'}

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
            >>> sorted(kwargs.items())
            [('id', 1), ('lang', 'en'), ('route_name', 'message')]

            Otherwise return (None, None)

            >>> r = PathRouter()
            >>> handler, kwargs = r.match(r'')
            >>> handler
            >>> kwargs
            {}
        """
        if path in self.path_map:
            return self.path_map[path]
        for route_match, handler in self.mapping:
            matched, kwargs = route_match(path)
            if matched >= 0:
                # TODO: isinstance(handler, PathRouter)
                handler_match = getattr(handler, 'match', None)
                if not handler_match:
                    return handler, kwargs
                handler, kwargs_inner = handler_match(
                    path[matched:])
                if handler:
                    if not kwargs:
                        return handler, kwargs_inner
                    if kwargs_inner:
                        kwargs = kwargs.copy()
                        merge(kwargs, kwargs_inner)
                    return handler, kwargs
        return None, {}

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
            ...     (r'{lang}/admin/', admin_routes, {'lang': 'en'})
            ... ])
            >>> r.path_for(r'signin')
            'en/admin/login'

            >>> r = PathRouter()
            >>> admin_routes = [
            ...     (r'', Login, None, 'signin')
            ... ]
            >>> r.add_routes([
            ...     (r'{lang}/', admin_routes, {'lang': 'en'})
            ... ])
            >>> r.path_for(r'signin')
            'en'

            Otherwise None

            >>> r.path_for(r'unknown')
        """
        if name in self.route_map:
            return self.route_map[name](kwargs).rstrip('/')
        else:
            try:
                return ''.join([path(kwargs) for path
                                in self.inner_route_map[name]]).rstrip('/')
            except KeyError:
                return None
