from builders import build_route
from config import route_builders as default_route_builders
from utils import camelcase_to_underscore, strip_name


class PathRouter(object):
    
    def __init__(self, route_builders = None):
        self.mapping = []
        self.route_map = {}
        self.route_builders = route_builders or default_route_builders

    def add_route(self, pattern, handler_class):
        handler_name = camelcase_to_underscore(
                strip_name(handler_class.__name__))
        route = build_route(pattern, self.route_builders)
        self.route_map[handler_name] = route
        self.mapping.append((route, handler_class))

    def add_routes(self, mapping):
        """ Adds routes represented as a list of tuple 
            (pattern, handler_class) to route table

            >>> r = PathRouter()
            >>> class Login: pass
            >>> class Message: pass
            >>> r.add_routes([(r'login', Login)])
            >>> len(r.mapping)
            1
            >>> len(r.route_map)
            1
        """
        for pattern, handler_class in mapping:
            self.add_route(pattern, handler_class)

    def match(self, path):
        """ Tries to find a match for the given path in route table.
            Returns a tupple of (handler_class, kwargs)

            >>> r = PathRouter()
            >>> class Login: pass
            >>> r.add_route(r'login', Login)
            >>> handler_class, kwargs = r.match(r'login')
            >>> assert handler_class
            >>> kwargs

            Otherwise return (None, None)

            >>> r = PathRouter()
            >>> handler_class, kwargs = r.match(r'')
            >>> handler_class
            >>> kwargs
        """
        for route, handler_class in self.mapping:
            succeed, kwargs = route.match(path)
            if succeed:
                return handler_class, kwargs
        return None, None

    def path_for(self, name, **kargs):
        """ Returns the url for given handler name.

            >>> r = PathRouter()
            >>> class Login: pass
            >>> r.add_route(r'login', Login)
            >>> r.path_for(r'login')
            'login'
            >>> r.path_for(r'unknown')
        """
        route = self.route_map.get(name, None)
        return route and route.path(kargs) or None


