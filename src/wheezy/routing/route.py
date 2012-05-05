
""" ``route`` module.
"""

import re

from wheezy.routing.utils import merge
from wheezy.routing.utils import outer_split


class Route(object):
    """ Route abstract contract.
    """
    __slots__ = ()

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


class PlainRoute(object):
    """ Route based on string equalty operation.
    """
    __slots__ = ('pattern', 'kwargs', 'matched', 'match')

    def __init__(self, pattern, finishing, kwargs=None):
        """ Initializes the route by given ``pattern``. If
            ``finishing`` is True than choose ``equals_math``
            strategy

            >>> r = PlainRoute(r'abc', True)
            >>> assert r.match == r.equals_match

            Otherwise ``startswith_match`` strategy is selected.

            >>> r = PlainRoute(r'abc', False)
            >>> assert r.match == r.startswith_match
        """
        self.pattern = pattern
        self.kwargs = kwargs
        self.matched = len(pattern)
        # Choose match strategy
        self.match = finishing and self.equals_match \
                or self.startswith_match

    def equals_match(self, path):
        """ If the ``path`` exactly equals pattern string,
            return end index of substring matched and a copy
            of ``self.kwargs``.

            >>> r = PlainRoute(r'abc', True)
            >>> matched, kwargs = r.equals_match('abc')
            >>> matched
            3
            >>> kwargs

            Match returns ``self.kwargs``.

            >>> r = PlainRoute(r'abc', True, {'a': 1})
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

            >>> r = PlainRoute(r'abc', False)
            >>> matched, kwargs = r.startswith_match('abc')
            >>> matched
            3
            >>> kwargs

            Match returns ``self.kwargs``.

            >>> r = PlainRoute(r'abc', False, {'a': 1})
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

            >>> r = PlainRoute(r'abc', True)
            >>> r.path()
            'abc'
        """
        return self.pattern


RE_SPLIT = re.compile(r'\<(\w+)\>')


def parse_pattern(pattern, value_provider):
    """
        >>> f = lambda v: '{%s}' % v
        >>> parse_pattern('abc/(?P<id>[^/]+)', f)
        ['abc/', '{id}']
        >>> parse_pattern('abc/(?P<n>[^/]+)/(?P<x>\\\w+)', f)
        ['abc/', '{n}', '/', '{x}']
        >>> parse_pattern('(?P<locale>(en|ru))/home', f)
        ['', '{locale}', '/home']

        >>> from wheezy.routing.curly import convert
        >>> parse_pattern(convert('[{locale:(en|ru)}/]home'), f)
        ['', '{locale}', '/home']
        >>> parse_pattern(convert('item[/{id:i}]'), f)
        ['item/', '{id}']

        >> p = convert(r'{controller:w}[/{action:w}[/{id:i}]]')
        >> parse_pattern(p, f)
        ['', '{controller}', '/', '{action}', '/', '{id}']
    """
    pattern = strip_optional(pattern)
    parts = outer_split(pattern, sep='()')
    if len(parts) % 2 == 1 and not parts[-1]:
        parts = parts[:-1]
    parts[1::2] = [value_provider(RE_SPLIT.split(p)[1])
            for p in parts[1::2]]
    return parts


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
    __slots__ = ('match', 'path', 'parts', 'kwargs', 'regex')

    def __init__(self, pattern, finishing, kwargs=None):
        pattern = pattern.lstrip('^').rstrip('$')
        # Choose match strategy
        if kwargs:
            def value_provider(name):
                kwargs.setdefault(name, '')
                return lambda values: str(values[name])
            self.match = self.match_with_kwargs
            self.path = self.path_with_kwargs
        else:
            def value_provider(name):
                return lambda values: str(values.get(name, ''))
            self.match = self.match_no_kwargs
            self.path = self.path_no_kwargs

        self.parts = parse_pattern(pattern, value_provider)
        pattern = '^' + pattern
        if finishing:
            pattern = pattern + '$'
        self.kwargs = kwargs
        self.regex = re.compile(pattern)

    def match_no_kwargs(self, path):
        """ If the ``path`` match the regex pattern.

            >>> r = RegexRoute(r'abc/(?P<id>\d+$)', True)
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

            >>> r = RegexRoute(r'abc/\d+', False, {'lang': 'en'})
            >>> matched, kwargs = r.match_with_kwargs('abc/1234')
            >>> matched
            8
            >>> kwargs
            {'lang': 'en'}

            >>> r = RegexRoute(r'abc/(?P<id>\d+$)', True, {
            ...     'lang': 'en'
            ... })
            >>> matched, kwargs = r.match_with_kwargs('abc/1234')
            >>> kwargs
            {'lang': 'en', 'id': '1234'}

            ``kwargs`` from ``pattern`` match must override
            defaults.

            >>> r = RegexRoute(r'abc/?(?P<id>\d*$)', True, {'id': '1'})
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
            return (m.end(), merge(self.kwargs.copy(), kwargs))
        return -1, None

    def path_no_kwargs(self, values=None):
        """ Build the path for the given route by substituting
            the named places of the regual expression.

            >>> r = RegexRoute(
            ...     r'abc/(?P<month>\d+)/(?P<day>\d+)',
            ...     True
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
        parts = self.parts[:]
        parts[1::2] = [f(values) for f in parts[1::2]]
        return ''.join(parts)

    def path_with_kwargs(self, values=None):
        """ Build the path for the given route by substituting
            the named places of the regual expression.

            >>> r = RegexRoute(
            ...     r'abc/(?P<month>\d+)/(?P<day>\d+)',
            ...     True,
            ...     dict(month=1, day=1)
            ... )
            >>> r.path_with_kwargs(dict(month=6, day=9))
            'abc/6/9'
            >>> r.path_with_kwargs(dict(month=6))
            'abc/6/1'
            >>> r.path()
            'abc/1/1'
        """
        if values:
            values = dict(self.kwargs, **values)
        else:
            values = self.kwargs
        parts = self.parts[:]
        parts[1::2] = [f(values) for f in parts[1::2]]
        return ''.join(parts)
