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

    def __init__(self, pattern, equals = True):
        """ Initializes the route by given ``pattern``. If ``equals``
            is True (this is default) than equals_match strategy is 
            selected. 

            >>> r = PlainRoute(r'abc', equals = True)
            >>> assert r.match == r.equals_match
            
            Otherwise startswith_match strategy is choosen 
            (``equals`` = False).

            >>> r = PlainRoute(r'abc', equals = False)
            >>> assert r.match == r.startswith_match
        """
        self.pattern = pattern.lower()
        self.matched = len(pattern)
        # Choose match strategy
        self.match = equals and self.equals_match or self.startswith_match

    def equals_match(self, path):
        """ If the ``path`` exactly equals pattern string, return the end
            of substring matched and None.

            >>> r = PlainRoute(r'abc')
            >>> matched, kwargs = r.equals_match('abc')
            >>> matched
            3
            >>> kwargs
            
            Otherwise return ``(-1, None)``.

            >>> matched, kwargs = r.equals_match('abc/')
            >>> matched
            -1
            >>> kwargs
            >>> matched, kwargs = r.startswith_match('bc')
            >>> matched
            -1
            >>> kwargs
        """
        return path == self.pattern and (self.matched, None) or (-1, None)

    def startswith_match(self, path):
        """ If the ``path`` starts with pattern string, return the end of
            substring matched and None.

            >>> r = PlainRoute(r'abc')
            >>> matched, kwargs = r.startswith_match('abc')
            >>> matched
            3
            >>> kwargs
            >>> matched, kwargs = r.startswith_match('abc/')
            >>> matched
            3
            >>> kwargs
            
            Otherwise return ``(None, None)``.

            >>> matched, kwargs = r.startswith_match('bc')
            >>> matched
            -1
            >>> kwargs
        """
        return path.startswith(self.pattern) and (self.matched, None) \
                or (-1, None)

    def path(self, values = None):
        """ Build the path for given route by simply returning the pattern 
            used during initialization.

            >>> r = PlainRoute(r'abc')
            >>> r.path()
            'abc'
        """
        return self.pattern

