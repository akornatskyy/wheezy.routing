import re


RE_STRIP_NAME = re.compile(r'(Handler|Controller)$')
RE_CAMELCASE_TO_UNDERSCOPE_1 = re.compile('(.)([A-Z][a-z]+)')
RE_CAMELCASE_TO_UNDERSCOPE_2 = re.compile('([a-z0-9])([A-Z])')


def route_name(handler):
    """ Return a name for the given handler.
        ``handler`` can be an object, class or callable.

        >>> class Login: pass
        >>> route_name(Login)
        'login'
    """

    try:
        name = handler.__name__
    except AttributeError:
        name = handler.__class__.__name__

    return camelcase_to_underscore(strip_name(name))


def strip_name(s):
    """ Strips the name per RE_STRIP_NAME regex.

        >>> strip_name('Login')
        'Login'
        >>> strip_name('LoginHandler')
        'Login'
        >>> strip_name('LoginController')
        'Login'
        >>> strip_name('LoginHandler2')
        'LoginHandler2'
    """
    return RE_STRIP_NAME.sub('', s)


def camelcase_to_underscore(s):
    """ Convert CamelCase to camel_case.
        >>> camelcase_to_underscore('MainPage')
        'main_page'
        >>> camelcase_to_underscore('Login')
        'login'
    """
    s = RE_CAMELCASE_TO_UNDERSCOPE_1.sub(r'\1_\2', s)
    return RE_CAMELCASE_TO_UNDERSCOPE_2.sub(r'\1_\2', s).lower()


def merge(d1, d2):
    """ Update ``d1`` from ``d2`` only if a value in ``d2``
        is evaluated to boolean True.

        >>> d1 = dict(a=1,b=None,c=2)
        >>> d2 = dict(a=None,b=2,c=1)
        >>> merge(d1, d2)
        {'a': 1, 'c': 1, 'b': 2}
    """
    d1.update(((k, v) for k, v in d2.iteritems() if v))
    return d1
