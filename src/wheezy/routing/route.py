
""" ``route`` module.
"""

import re

from utils import merge


class Route(object):
    """ Route abstract contract.
    """

    def match(self, path):
        """ if the ``path`` matches, return the end of substring matched
            and a copy of kwargs. Otherwise return ``(-1, None)``.

            >>> r = Route()
            >>> matched, kwargs = r.match('x')
            Traceback (most recent call last):
                ...
            NotImplementedError
        """
        raise NotImplementedError()

    def path(self, values=None):
        """ Build the path for given route.

            >>> r = Route()
            >>> r.path(dict(id=1234))
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
        """ If the ``path`` exactly equals pattern string,
            return end index of substring matched and a copy
            of ``self.kwargs``.

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
        return path == self.pattern and \
            (self.matched, self.kwargs) or (-1, None)

    def startswith_match(self, path):
        """ If the ``path`` starts with pattern string, return
            the end of substring matched and ``self.kwargs``.

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
        return path.startswith(self.pattern) and \
            (self.matched, self.kwargs) or (-1, None)

    def path(self, values=None):
        """ Build the path for given route by simply returning
            the pattern used during initialization.

            >>> r = PlainRoute(r'abc')
            >>> r.path()
            'abc'
        """
        return self.pattern


class RegexRoute(object):
    """ Route based on regular expression matching.
    """

    RE_SPLIT = re.compile(r'\(\?P(\<\w+\>).+?\)')

    def __init__(self, pattern, kwargs=None):
        """
        """
        self.pattern = pattern
        self.kwargs = kwargs
        self.regex = re.compile(pattern)

        def f(value):
            if value.startswith('<') and value.endswith('>'):
                value = value[1:-1]
                return lambda values: str(values.get(value, ''))
            else:
                return value

        split = RegexRoute.RE_SPLIT.split(pattern)
        self.parts = tuple((f(v) for v in split if v))
        # Choose match strategy
        if kwargs:
            self.match = self.match_with_kwargs
            self.path = self.path_with_kwargs
        else:
            self.match = self.match_no_kwargs
            self.path = self.path_no_kwargs

    def match_no_kwargs(self, path):
        """ If the ``path`` match the regex pattern.

            >>> r = RegexRoute(r'abc/(?P<id>\d+$)')
            >>> matched, kwargs = r.match_no_kwargs('abc/1234')
            >>> matched
            8
            >>> kwargs
            {'id': '1234'}

            Otherwise return ``(-1, None)``.

            >>> matched, kwargs = r.match_no_kwargs('abc/x')
            >>> matched
            -1
            >>> kwargs
        """
        m = self.regex.match(path)
        if m:
            return m.end(), m.groupdict()
        return -1, None

    def match_with_kwargs(self, path):
        """ If the ``path`` match the regex pattern.

            >>> r = RegexRoute(r'abc/\d+', {'lang': 'en'})
            >>> matched, kwargs = r.match_with_kwargs('abc/1234')
            >>> matched
            8
            >>> kwargs
            {'lang': 'en'}

            >>> r = RegexRoute(r'abc/(?P<id>\d+$)', {
            ...     'lang': 'en'
            ... })
            >>> matched, kwargs = r.match_with_kwargs('abc/1234')
            >>> kwargs
            {'lang': 'en', 'id': '1234'}

            ``kwargs`` from ``pattern`` match must override
            defaults.

            >>> r = RegexRoute(r'abc/?(?P<id>\d*$)', {'id': '1'})
            >>> matched, kwargs = r.match_with_kwargs('abc')
            >>> kwargs
            {'id': '1'}
            >>> matched, kwargs = r.match_with_kwargs('abc/1234')
            >>> kwargs
            {'id': '1234'}

            Otherwise return ``(-1, None)``.

            >>> matched, kwargs = r.match_with_kwargs('abc/x')
            >>> matched
            -1
            >>> kwargs
        """
        m = self.regex.match(path)
        if m:
            kwargs = m.groupdict()
            return (m.end(), not kwargs and self.kwargs or merge(
                        self.kwargs.copy(), kwargs))
        return -1, None

    def path_no_kwargs(self, values=None):
        """ Build the path for the given route by substituting
            the named places of the regual expression.

            >>> r = RegexRoute(
            ...     r'abc/(?P<month>\d+)/(?P<day>\d+)'
            ... )
            >>> r.path_no_kwargs(dict(month = 6, day = 9))
            'abc/6/9'
            >>> r.path_no_kwargs(dict(month = 6))
            'abc/6'
            >>> r.path()
            'abc'
        """

        if values is None:
            values = {}
        parts = (isinstance(f, basestring) and f or f(values)
                for f in self.parts)
        return ''.join(parts).rstrip('/')

    def path_with_kwargs(self, values=None):
        """ Build the path for the given route by substituting
            the named places of the regual expression.

            >>> r = RegexRoute(
            ...     r'abc/(?P<month>\d+)/(?P<day>\d+)',
            ...     dict(month=1, day=1)
            ... )
            >>> r.path_with_kwargs(dict(month=6, day=9))
            'abc/6/9'
            >>> r.path_with_kwargs(dict(month=6))
            'abc/6/1'
            >>> r.path()
            'abc/1/1'
        """

        values = not values and self.kwargs or merge(
                self.kwargs.copy(), values)
        parts = (isinstance(f, basestring) and f or f(values)
                for f in self.parts)
        return ''.join(parts).rstrip('/')
