
""" ``curly`` module.
"""

import re


RE_SPLIT = re.compile('(?P<n>\{[\w:]+\})')

patterns = {
    # one or more digits
    'i': r'\d+',
    'int': r'\d+',
    'number': r'\d+',
    'digits': r'\d+',
    # one or more word characters
    'w': r'\w+',
    'word': r'\w+',
    # everything until ``/``
    's': r'[^/]+',
    'segment': r'[^/]+',
    'part': r'[^/]+',
    # any
    'a': r'.+',
    'any': r'.+',
    'rest': r'.+'
}

default_pattern = 's'


def convert(s):
    """ Convert curly expression into regex with
        named groups.

        >>> convert(r'abc/{id}')
        'abc/(?P<id>[^/]+)'

        >>> convert(r'abc/{id:i}')
        'abc/(?P<id>\\\d+)'

        >>> convert(r'abc/{n}/{x:w}')
        'abc/(?P<n>[^/]+)/(?P<x>\\\w+)'
    """
    parts = RE_SPLIT.split(s)
    return ''.join(map(replace, parts))


def replace(val):
    """ Replace ``{group_name:pattern_name}`` by regex with
        named groups.

        If the ``val`` is not an expression in curly brackets
        simply return it.
        >>> replace('abc')
        'abc'

        If the ``pattern_name`` is not specified, use
        default one.

        >>> replace('{abc}')
        '(?P<abc>[^/]+)'

        Replace the ``pattern_name`` with regex from
        ``patterns`` dict.

        >>> replace('{abc:i}')
        '(?P<abc>\\\d+)'

        The ``pattern_name`` not found raise ``KeyError``.

        >>> replace('{abc:x}')
        Traceback (most recent call last):
            ...
        KeyError: 'x'
    """
    if val.startswith('{') and val.endswith('}'):
        group_name, pattern_name = parse(val[1:-1])
        pattern = patterns[pattern_name]
        return '(?P<%s>%s)' % (group_name, pattern)
    return val


def parse(s):
    """ Parse ``s`` according to ``group_name:pattern_name``.

        There is just ``group_name``, return default
        ``pattern_name``.
        >>> parse('abc')
        ('abc', 's')

        Otherwise both.
        >>> parse('abc:i')
        ('abc', 'i')
    """
    if ':' in s:
        return tuple(s.split(':', 1))
    return s, default_pattern
