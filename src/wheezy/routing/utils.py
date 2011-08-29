import re


RE_CAMELCASE_TO_UNDERSCOPE = \
        re.compile(r'(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))')

RE_STRIP_NAME = \
        re.compile(r'(Handler|Controller)$')


def strip_name(s):
    """ Strips the name per 

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
    return RE_CAMELCASE_TO_UNDERSCOPE.sub('_\\1', s).lower()[1:]


