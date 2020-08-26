""" ``utils`` module.
"""

import re

RE_STRIP_NAME = re.compile(r"(Handler|Controller|Page|View)$")
RE_CAMELCASE_TO_UNDERSCOPE_1 = re.compile("(.)([A-Z][a-z]+)")
RE_CAMELCASE_TO_UNDERSCOPE_2 = re.compile("([a-z0-9])([A-Z])")


def route_name(handler):
    """Return a name for the given handler.
    ``handler`` can be an object, class or callable.

    >>> class Login: pass
    >>> route_name(Login)
    'login'
    >>> l = Login()
    >>> route_name(l)
    'login'
    """

    try:
        name = handler.__name__
    except AttributeError:
        name = handler.__class__.__name__

    return camelcase_to_underscore(strip_name(name))


def strip_name(s):
    """Strips the name per RE_STRIP_NAME regex.

    >>> strip_name('Login')
    'Login'
    >>> strip_name('LoginHandler')
    'Login'
    >>> strip_name('LoginController')
    'Login'
    >>> strip_name('LoginPage')
    'Login'
    >>> strip_name('LoginView')
    'Login'
    >>> strip_name('LoginHandler2')
    'LoginHandler2'
    """
    return RE_STRIP_NAME.sub("", s)


def camelcase_to_underscore(s):
    """Convert CamelCase to camel_case.

    >>> camelcase_to_underscore('MainPage')
    'main_page'
    >>> camelcase_to_underscore('Login')
    'login'
    """
    s = RE_CAMELCASE_TO_UNDERSCOPE_1.sub(r"\1_\2", s)
    return RE_CAMELCASE_TO_UNDERSCOPE_2.sub(r"\1_\2", s).lower()


def outer_split(expression, sep="()"):
    """Splits given ``expression`` by outer most separators.

    >>> outer_split('123')
    ['123']
    >>> outer_split('123(45(67)89)123(45)67')
    ['123', '45(67)89', '123', '45', '67']

    If expression is not balanced raises ``ValueError``.

    >>> outer_split('123(') # doctest: +ELLIPSIS
    Traceback (most recent call last):
        ...
    ValueError: ...
    """
    assert 2 == len(sep)
    start_sep, end_sep = sep
    start_count = end_count = 0
    parts = []
    part = ""
    for token in expression:
        if token == start_sep:
            if start_count == end_count:
                parts.append(part)
                part = ""
                start_count += 1
                continue
            start_count += 1
        elif token == end_sep:
            end_count += 1
            if start_count == end_count:
                parts.append(part)
                part = ""
                continue
        part += token
    if start_count != end_count:
        raise ValueError("Expression is not balanced")
    parts.append(part)
    return parts
