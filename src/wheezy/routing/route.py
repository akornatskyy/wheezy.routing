class Route(object):
    """ Route abstract contract.
    """

    def match(self, path):
        """ if the ``path`` matches, return the end of substring matched, the
            dictionary of kwargs. Otherwise return ``(-1, None)``.

            >>> r = Route()
            >>> matched, kwargs = r.match('x')
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

    def __init__(self, pattern, kwargs=None):
        """ Initializes the route by given ``pattern``. If 
            pattern ends with ``/`` than it select ``startswith``
            strategy. 

            >>> r = PlainRoute(r'abc/')
            >>> assert r.match == r.startswith_match
            
            Otherwise ``equals`` strategy is selected.

            >>> r = PlainRoute(r'abc')
            >>> assert r.match == r.equals_match
        """
        self.pattern = pattern
        self.kwargs = kwargs
        self.matched = len(pattern)
        # Choose match strategy
        self.match = pattern[-1:] == '/' \
                and self.startswith_match \
                or self.equals_match

    def equals_match(self, path):
        """ If the ``path`` exactly equals pattern string, return the end
            of substring matched and ``self.kwargs``.

            >>> r = PlainRoute(r'abc')
            >>> matched, kwargs = r.equals_match('abc')
            >>> matched
            3
            >>> kwargs

            Match returns ``self.kwargs``.

            >>> r = PlainRoute(r'abc', {'a': 1})
            >>> matched, kwargs = r.equals_match('abc')
            >>> matched
            3
            >>> kwargs
            {'a': 1}
            
            Otherwise return ``(-1, None)``.

            >>> matched, kwargs = r.equals_match('abc/')
            >>> matched
            -1
            >>> matched, kwargs = r.equals_match('bc')
            >>> matched
            -1
            >>> kwargs
        """
        return path == self.pattern \
                and (self.matched, self.kwargs) or (-1, None)

    def startswith_match(self, path):
        """ If the ``path`` starts with pattern string, return the end of
            substring matched and ``self.kwargs``.

            >>> r = PlainRoute(r'abc')
            >>> matched, kwargs = r.startswith_match('abc')
            >>> matched
            3
            >>> kwargs

            Match returns ``self.kwargs``.

            >>> r = PlainRoute(r'abc', {'a': 1})
            >>> matched, kwargs = r.startswith_match('abc/')
            >>> matched
            3
            >>> kwargs
            {'a': 1}

            Otherwise return ``(None, None)``.

            >>> matched, kwargs = r.startswith_match('bc')
            >>> matched
            -1
            >>> kwargs
        """
        return path.startswith(self.pattern) \
                and (self.matched, self.kwargs) or (-1, None)

    def path(self, values = None):
        """ Build the path for given route by simply returning the pattern 
            used during initialization.

            >>> r = PlainRoute(r'abc')
            >>> r.path()
            'abc'
        """
        return self.pattern

