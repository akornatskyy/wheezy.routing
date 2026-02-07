import unittest

from wheezy.routing.plain import PlainRoute, try_build_plain_route


class TryPlainRouteTestCase(unittest.TestCase):
    def test_build(self):
        """Ensure plain route is built."""
        route = try_build_plain_route("favicon.ico")
        assert route
        assert route == try_build_plain_route(route)
        assert not try_build_plain_route(".*")


class PlainRouteTestCase(unittest.TestCase):
    def test_match_finishing(self):
        """Equals match strategy."""
        r = PlainRoute("abc", finishing=True, kwargs={"x": 2}, name="test")

        assert 1 == len(r.exact_matches)
        pattern, kwargs = r.exact_matches[0]
        assert "abc" == pattern
        assert [("route_name", "test"), ("x", 2)] == sorted(kwargs.items())
        matched, kwargs = r.match("abc")
        assert 3 == matched
        assert [("route_name", "test"), ("x", 2)] == sorted(kwargs.items())

        assert (-1, None) == r.match("ab")
        r.exact_matches = None

    def test_match_intermediate(self):
        """Starts with strategy."""
        r = PlainRoute("abc", finishing=False, kwargs={"x": 2}, name="ignore")

        assert (("abc", {"x": 2}),) == r.exact_matches
        matched, kwargs = r.match("abcd")
        assert 3 == matched
        assert [("x", 2)] == sorted(kwargs.items())

        matched, kwargs = r.match("ab")
        r.exact_matches = None

    def test_path(self):
        """Returns pattern."""
        r = PlainRoute("abc", finishing=False, kwargs={}, name=None)
        assert "abc" == r.path()
