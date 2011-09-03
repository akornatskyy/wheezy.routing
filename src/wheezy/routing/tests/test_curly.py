
""" Unit tests for ``wheezy.routing.curly``.
"""

import unittest


class PatternsTestCase(unittest.TestCase):
    """ Test the ``curly.patterns`` dict.
    """

    def test_values(self):
        """ Ensure patterns values are valid regex.
        """
        import re

        from wheezy.routing.curly import patterns

        for p in patterns.itervalues():
            assert re.compile(p)

    def test_default(self):
        """ Make sure ``default_pattern`` is in ``patterns``.
        """
        from wheezy.routing.curly import patterns
        from wheezy.routing.curly import default_pattern

        assert default_pattern in patterns


class ConvertTestCase(unittest.TestCase):
    """ Test the ``curly.convert`` function.
    """

    def test_sigle_group_name(self):
        """ A single group name.
        """
        from wheezy.routing.curly import convert

        pattern = convert(r'abc/{id}')

        self.assertEquals('abc/(?P<id>[^/]+)', pattern)

    def test_two_groups(self):
        """ Take two group names.
        """
        from wheezy.routing.curly import convert

        pattern = convert(r'abc/{n1}/{n2}')

        self.assertEquals(
            'abc/(?P<n1>[^/]+)/(?P<n2>[^/]+)',
            pattern
        )


class ReplaceTestCase(unittest.TestCase):
    """ Test the ``curly.replace`` function.
    """

    def test_no_curly_brackets(self):
        """ ``val`` is not an expression in curly brackets.
        """
        from wheezy.routing.curly import replace

        p = replace('abc')

        self.assertEquals('abc', p)

    def test_group_name_only(self):
        """ ``val`` has group name only.
        """
        from wheezy.routing.curly import replace

        p = replace('{abc}')

        self.assertEquals('(?P<abc>[^/]+)', p)

    def test_pattern_name(self):
        """ ``val`` has pattern name.
        """
        from wheezy.routing.curly import replace

        p = replace('{abc:int}')

        self.assertEquals(r'(?P<abc>\d+)', p)

    def test_unknown_pattern_name(self):
        """ ``val`` has pattern name that is unknown.
        """
        from wheezy.routing.curly import replace

        self.assertRaises(
                KeyError,
                lambda: replace('{abc:x}')
        )


class ParseTestCase(unittest.TestCase):
    """ Test the ``curly.parse`` function.
    """

    def test_no_colon(self):
        """ there is no colon in input string
        """
        from wheezy.routing.curly import parse
        from wheezy.routing import config

        group_name, pattern_name = parse('abc')

        self.assertEquals('abc', group_name)
        self.assertEquals('s', pattern_name)
        self.assertEquals(
                config.curly_default_pattern,
                pattern_name
        )

    def test_with_colon(self):
        """ there is colon in input string
        """
        from wheezy.routing.curly import parse
        from wheezy.routing import config

        group_name, pattern_name = parse('abc:i')

        self.assertEquals('abc', group_name)
        self.assertEquals('i', pattern_name)
