""" Unit tests for ``wheezy.routing.curly``.
"""

import re
import unittest

from wheezy.routing import config
from wheezy.routing.curly import (
    convert,
    default_pattern,
    parse,
    patterns,
    replace,
    try_build_curly_route,
)


class TryBuildCurlyRouteTestCase(unittest.TestCase):
    def test_build(self):
        """Ensure curly route is built."""
        route = try_build_curly_route("{locale:(en|ru)}")
        assert route
        assert route == try_build_curly_route(route)
        assert not try_build_curly_route(".*")


class PatternsTestCase(unittest.TestCase):
    """Test the ``curly.patterns`` dict."""

    def test_values(self):
        """Ensure patterns values are valid regex."""
        for p in patterns.values():
            assert re.compile(p)

    def test_default(self):
        """Make sure ``default_pattern`` is in ``patterns``."""
        assert default_pattern in patterns

    def test_synonyms(self):
        """Make sure ``default_pattern`` is in ``patterns``."""
        self.assertEquals(13, len(patterns))
        synonyms_map = (
            ("i", ("int", "digits", "number")),
            ("w", ("word",)),
            ("s", ("segment", "part")),
            ("a", ("any", "rest", "*")),
        )

        for n, syns in synonyms_map:
            pattern = patterns[n]
            for s in syns:
                assert pattern == patterns[s]


class ConvertTestCase(unittest.TestCase):
    """Test the ``curly.convert`` function."""

    def test_sigle_group_name(self):
        """A single group name."""
        pattern = convert(r"abc/{id}")

        self.assertEquals("abc/(?P<id>[^/]+)", pattern)

    def test_two_groups(self):
        """Take two group names."""
        pattern = convert(r"abc/{n1}/{n2:s}")

        self.assertEquals("abc/(?P<n1>[^/]+)/(?P<n2>[^/]+)", pattern)


class ReplaceTestCase(unittest.TestCase):
    """Test the ``curly.replace`` function."""

    def test_no_curly_brackets(self):
        """``val`` is not an expression in curly brackets."""
        p = replace("abc")

        self.assertEquals("abc", p)

    def test_group_name_only(self):
        """``val`` has group name only."""
        p = replace("{abc}")

        self.assertEquals("(?P<abc>[^/]+)", p)

    def test_pattern_name(self):
        """``val`` has pattern name."""
        p = replace("{abc:int}")

        self.assertEquals(r"(?P<abc>\d+)", p)

    def test_unknown_pattern_name(self):
        """``val`` has pattern name that is unknown."""
        p = replace("{abc:(x|y)}")

        self.assertEquals(r"(?P<abc>(x|y))", p)


class ParseTestCase(unittest.TestCase):
    """Test the ``curly.parse`` function."""

    def test_no_colon(self):
        """there is no colon in input string"""
        group_name, pattern_name = parse("abc")

        self.assertEquals("abc", group_name)
        self.assertEquals("s", pattern_name)
        self.assertEquals(config.curly_default_pattern, pattern_name)

    def test_with_colon(self):
        """there is colon in input string"""
        group_name, pattern_name = parse("abc:i")

        self.assertEquals("abc", group_name)
        self.assertEquals("i", pattern_name)
