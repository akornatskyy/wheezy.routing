""" Unit test for ``wheezy.routing.router``.
"""

import unittest

from mock import Mock


class RouterTestCase(unittest.TestCase):
    def setUp(self):
        from wheezy.routing.router import PathRouter

        self.mock_builder = Mock()
        self.r = PathRouter(route_builders=[self.mock_builder])

    def test_add_route_no_exact_matches(self):
        """No exact matches."""
        mock_route = Mock()
        mock_route.exact_matches = None
        self.mock_builder.return_value = mock_route

        self.r.add_route("pa", "handler", {}, "a")
        self.mock_builder.assert_called_once_with("pa", True, {}, "a")
        assert "a" in self.r.path_map
        assert self.r.mapping

    def test_add_route_with_exact_matches(self):
        """With exact matches."""
        mock_route = Mock()
        mock_route.exact_matches = [("pa", {})]
        self.mock_builder.return_value = mock_route

        self.r.add_route("pa", "handler", {}, "a")
        self.mock_builder.assert_called_once_with("pa", True, {}, "a")
        assert "a" in self.r.path_map
        assert "pa" in self.r.match_map

    def test_include_no_exact_matches(self):
        """Multilevel include."""
        mock_route = Mock()
        mock_route.exact_matches = None
        self.mock_builder.return_value = mock_route

        error_urls = [("401", "handler", {}, "http401"), ("402", "handler")]
        all_urls = [("error", error_urls, None)]
        self.r.include("pa", all_urls, {})
        assert "http401" in self.r.inner_path_map


class RouterMatchTestCase(unittest.TestCase):
    def setUp(self):
        from wheezy.routing.router import PathRouter

        self.r = PathRouter()

    def test_exact(self):
        self.r.add_route("", "h", name="root")
        assert ("h", {"route_name": "root"}) == self.r.match("")
        assert (None, {}) == self.r.match("x")

    def test_scan(self):
        self.r.add_route(".*", "h", name="all")
        assert ("h", {"route_name": "all"}) == self.r.match("")

    def test_scan_hierarchical(self):
        self.r.include("m/", [("{id}", "h", None, "msg")])

        handler, kwargs = self.r.match("m/123")
        assert "h" == handler
        assert [("id", "123"), ("route_name", "msg")] == sorted(kwargs.items())

        assert (None, {}) == self.r.match("x")

    def test_scan_hierarchical_merge(self):
        self.r.include("m/", [("{id}", "h", {"a": "2"}, "msg")], {"a": "1"})

        handler, kwargs = self.r.match("m/123")
        assert "h" == handler
        assert [("a", "2"), ("id", "123"), ("route_name", "msg")] == sorted(
            kwargs.items()
        )

        assert (None, {}) == self.r.match("x")


class RouterPathForTestCase(unittest.TestCase):
    def setUp(self):
        from wheezy.routing.router import PathRouter

        self.r = PathRouter()

    def test_exact(self):
        self.r.add_route(
            "/{locale:(en|ru)}/signin", "h", {"locale": "en"}, name="signin"
        )
        assert "/en/signin" == self.r.path_for("signin")
        assert "/ru/signin" == self.r.path_for("signin", locale="ru")
        self.assertRaises(KeyError, lambda: self.r.path_for("x"))

    def test_hierarchical(self):
        membership_urls = [("signin", "h", None, "signin")]

        self.r.include("/{locale:(en|ru)}/", membership_urls, {"locale": "en"})

        assert "/en/signin" == self.r.path_for("signin")
        self.assertRaises(KeyError, lambda: self.r.path_for("x"))


class UrlTestCase(unittest.TestCase):
    def test_url(self):
        """Check returns tuple."""
        from wheezy.routing.router import url

        assert ("pattern", "handler", "kwargs", "name") == url(
            "pattern", "handler", "kwargs", "name"
        )
