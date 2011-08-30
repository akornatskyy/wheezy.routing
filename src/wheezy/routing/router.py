from builders import build_route
from config import route_builders as default_route_builders
from utils import route_name


class PathRouter(object):
    
    def __init__(self, route_builders=None):
        self.mapping = []
        self.route_map = {}
        self.routers = []
        self.route_builders = route_builders or default_route_builders

    def add_route(self, pattern, handler_class, 
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
        handler_name = name or route_name(handler_class)
        route = build_route(pattern, kwargs, self.route_builders)
        self.route_map[handler_name] = route
        self.mapping.append((route, handler_class))

    def include(self, pattern, included, kwargs=None):
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
            >>> r.add_routes([(r'login', Login)])
            >>> len(r.mapping)
            1
            >>> len(r.route_map)
            1

            If ``handler`` is tuple, list or an instance of PathRouter
            than we proceed with ``add_include`` function

            >>> r = PathRouter()
            >>> class Login: pass
            >>> admin_routes = [(r'login', Login)]
            >>> r.add_routes([(r'admin/', admin_routes)])
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
            Returns a tupple of (handler_class, kwargs)

            >>> r = PathRouter()
            >>> class Login: pass
            >>> class Message: pass
            >>> r.add_route(r'login', Login)
            >>> handler_class, kwargs = r.match(r'login')
            >>> assert handler_class == Login
            >>> kwargs

            Tries to find inner match

            >>> r = PathRouter()
            >>> admin_routes = [(r'login', Login)]
            >>> r.add_routes([(r'admin/', admin_routes)])
            >>> handler_class, kwargs = r.match(r'admin/login')
            >>> assert handler_class == Login

            Merge kwargs

            >>> r = PathRouter()
            >>> admin_routes = [(r'msg', Message, {'id': 1})]
            >>> r.add_routes([(r'en/', admin_routes, {'lang': 'en'})])
            >>> handler_class, kwargs = r.match(r'en/msg')
            >>> assert handler_class == Message
            >>> kwargs
            {'lang': 'en', 'id': 1}

            Otherwise return (None, None)

            >>> r = PathRouter()
            >>> handler_class, kwargs = r.match(r'')
            >>> handler_class
            >>> kwargs
        """
        for route, handler_class in self.mapping:
            matched, kwargs = route.match(path)
            if matched >= 0:
                if isinstance(handler_class, PathRouter):
                    handler_class, kwargs2 = handler_class.match(
                            path[matched:])
                    if kwargs:
                        if kwargs2:
                            kwargs.update(kwargs2)
                    else:
                        kwargs = kwargs2
                return handler_class, kwargs
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
            >>> admin_routes = [(r'login', Login, None, 'signin')]
            >>> r.add_routes([(r'admin/', admin_routes)])
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
        else:
            return None
