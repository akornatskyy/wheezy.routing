class Route(object):
    """ Route abstract contract.
    """

    def match(self, path):
        """ if the ``path`` matches, return the boolean succeed, the
            dictionary of kwargs. Otherwise return ``(None, None)``.

            >>> r = Route()
            >>> r.match('x')
            Traceback (most recent call last):
                ...
            NotImplementedError
        """
        raise NotImplementedError()

    def path(self, values = None):
        """ Build the path for given route.

            >>> r = Route()
            >>> r.path(dict(id = 1234))
            Traceback (most recent call last):
                ...
            NotImplementedError
        """
        raise NotImplementedError()


class PlainRoute(Route):
    """ Route based on string equalty operation.
    """

    def __init__(self, pattern):
        self.pattern = pattern.lower()

    def match(self, path):
        """ If the ``path`` exactly equals pattern string, return the boolean
            succeed, None.

            >>> r = PlainRoute(r'abc')
            >>> succeed, kwargs = r.match('abc')
            >>> succeed
            True
            >>> kwargs
            
            Otherwise return ``(None, None)``.

            >>> succeed, kwargs = r.match('bc')
            >>> succeed
            False
            >>> kwargs
        """
        return path == self.pattern, None

    def path(self, values = None):
        """ Build the path for given route by simply returning the pattern 
            used during initialization.

            >>> r = PlainRoute(r'abc')
            >>> r.path()
            'abc'
        """
        return self.pattern
