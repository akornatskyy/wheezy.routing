
""" ``route`` module.
"""

import re

from wheezy.routing.comp import basestring
from wheezy.routing.utils import merge
from wheezy.routing.utils import outer_split


class Route(object):
    """ Route abstract contract.
    """

    def match(self, path):
        """ if the ``path`` matches, return the end of
            substring matched and kwargs. Otherwise
            return ``(-1, None)``.

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


RE_SPLIT = re.compile(r'\<(\w+)\>')


def parse_pattern(pattern, value_provider):
    """
        >>> f = lambda v: '{%s}' % v
        >>> parse_pattern('abc/(?P<id>[^/]+)', f)
        ('abc/', '{id}')
        >>> parse_pattern('abc/(?P<n>[^/]+)/(?P<x>\\\w+)', f)
        ('abc/', '{n}', '/', '{x}')
        >>> parse_pattern('(?P<locale>(en|ru))/home', f)
        ('{locale}', '/home')

        >>> from curly import convert
        >>> parse_pattern(convert('[{locale:(en|ru)}/]home'), f)
        ('{locale}', '/home')
        >>> parse_pattern(convert('item[/{id:i}]'), f)
        ('item/', '{id}')

        >> p = convert(r'{controller:w}[/{action:w}[/{id:i}]]')
        >> parse_pattern(p, f)
        ('{controller}', '/', '{action}', '/', '{id}')
    """
    pattern = strip_optional(pattern)
    parts = outer_split(pattern, sep='()')
    parts[::2] = [p.lstrip('?') for p in parts[::2]]
    parts[1::2] = [value_provider(RE_SPLIT.split(p)[1])
            for p in parts[1::2]]
    return tuple(v for v in parts if v)


def strip_optional(pattern):
    """
        at the beginning

        >>> strip_optional('((?P<locale>(en|ru))/)?home')
        '(?P<locale>(en|ru))/home'

        at the end

        >>> strip_optional('item(/(?P<id>\\\d+))?')
        'item/(?P<id>\\\d+)'

        nested:

        >>> p = '(?P<controller>\\\w+)(/(?P<action>\\\w+)(/(?P<id>\\\d+))?)?'
        >>> strip_optional(p)
        '(?P<controller>\\\w+)/(?P<action>\\\w+)/(?P<id>\\\d+)'
    """
    if ')?' not in pattern:
        return pattern
    parts = outer_split(pattern, sep='()')
    for i in range(2, len(parts), 2):
        part = parts[i]
        if part.startswith('?'):
            parts[i] = part[1:]
            parts[i - 1] = strip_optional(parts[i - 1])
        else:
            parts[i - 1] = "(%s)" % parts[i - 1]
    return ''.join(parts)


class RegexRoute(object):
    """ Route based on regular expression matching.
    """

    def __init__(self, pattern, kwargs=None):
        self.pattern = pattern
        self.kwargs = kwargs
        self.regex = re.compile(pattern)

        self.parts = parse_pattern(
                pattern,
                lambda name: lambda values: str(values.get(name, '')))
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
            >>> r.path_no_kwargs(dict(month=6, day=9))
            'abc/6/9'
            >>> r.path_no_kwargs(dict(month=6))
            'abc/6/'
            >>> r.path()  # stripped by router
            'abc//'
        """

        if values is None:
            values = {}
        parts = (isinstance(f, str) and f or f(values)
                for f in self.parts)
        return ''.join(parts)

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
        return ''.join(parts)
