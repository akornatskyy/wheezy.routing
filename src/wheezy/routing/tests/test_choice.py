""" Unit tests for ``wheezy.routing.plain``.
"""

import unittest


class TryChoiceRouteTestCase(unittest.TestCase):
    def test_build(self):
        """ Ensure choice route is built.
        """
        from wheezy.routing.choice import try_build_choice_route

        route = try_build_choice_route("{locale:(en|ru)}")
        assert route
        assert route == try_build_choice_route(route)
        assert not try_build_choice_route(".*")


class ChoiceRouteTestCase(unittest.TestCase):
    def test_match(self):
        """ Ensure matches.
        """
        from wheezy.routing.choice import ChoiceRoute

        r = ChoiceRoute("{locale:(en|ru)}/", True, {"x": "1"}, "test")

        matched, kwargs = r.match("en/")
        assert 3 == matched
        assert [
            ("locale", "en"),
            ("route_name", "test"),
            ("x", "1"),
        ] == sorted(kwargs.items())

        matched, kwargs = r.match("ru/")
        assert 3 == matched
        assert [
            ("locale", "ru"),
            ("route_name", "test"),
            ("x", "1"),
        ] == sorted(kwargs.items())

        assert (-1, None) == r.match("x")

    def test_path(self):
        """ Ensure path is built correctly.
        """
        from wheezy.routing.choice import ChoiceRoute

        r = ChoiceRoute("{locale:(en|ru)}/", True, {"locale": "en"}, "test")

        assert "ru/" == r.path({"locale": "ru"})
        assert "en/" == r.path()
