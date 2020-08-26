""" Unit tests for ``wheezy.routing.regex``.
"""

import unittest


class TryRegexRouteTestCase(unittest.TestCase):
    def test_build(self):
        """Ensure plain route is built."""
        from wheezy.routing.regex import try_build_regex_route

        route = try_build_regex_route(".*")
        assert route
        assert route == try_build_regex_route(route)


class RegexRouteTestCase(unittest.TestCase):
    def test_match_no_kwargs(self):
        from wheezy.routing.regex import RegexRoute

        r = RegexRoute(
            "abc/(?P<id>[^/]+)", finishing=True, kwargs=None, name="test"
        )
        matched, kwargs = r.match("abc/123")
        assert 7 == matched
        assert [("id", "123"), ("route_name", "test")] == sorted(
            kwargs.items()
        )

        assert (-1, None) == r.match("abc/")

        r = RegexRoute(
            "abc/(?P<id>[^/]+)", finishing=False, kwargs=None, name="ignore"
        )
        matched, kwargs = r.match("abc/123/info")
        assert 7 == matched
        assert {"id": "123"} == kwargs

        assert (-1, None) == r.match("abc/")

    def test_match_with_kwargs(self):
        from wheezy.routing.regex import RegexRoute

        defaults = {"lang": "en", "id": "0"}
        r = RegexRoute(
            "abc/(?P<id>[^/]+)", finishing=True, kwargs=defaults, name="test"
        )
        matched, kwargs = r.match("abc/123")
        assert 7 == matched
        assert [
            ("id", "123"),
            ("lang", "en"),
            ("route_name", "test"),
        ] == sorted(kwargs.items())

        assert (-1, None) == r.match("abc/")

        r = RegexRoute(
            "abc/(?P<id>[^/]+)",
            finishing=False,
            kwargs=defaults,
            name="ignore",
        )
        matched, kwargs = r.match("abc/123/info")
        assert 7 == matched
        assert [("id", "123"), ("lang", "en")] == sorted(kwargs.items())

        assert (-1, None) == r.match("abc/")

    def test_path_no_kwargs(self):
        from wheezy.routing.regex import RegexRoute

        r = RegexRoute(
            "abc/(?P<id>[^/]+)", finishing=True, kwargs=None, name="test"
        )

        assert "abc/123" == r.path({"id": "123"})

        self.assertRaises(KeyError, lambda: r.path({}))

    def test_path_with_kwargs(self):
        from wheezy.routing.regex import RegexRoute

        r = RegexRoute(
            "abc/(?P<id>[^/]+)",
            finishing=True,
            kwargs={"id": "1"},
            name="test",
        )

        assert "abc/123" == r.path({"id": "123"})
        assert "abc/1" == r.path()
