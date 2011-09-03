
""" Unit tests for ``wheezy.routing.builders``.
"""

import unittest

from mocker import Mocker, expect


class TryBuildPlainRouteTestCase(unittest.TestCase):
    """ Test the ``builders.try_build_plain_route``
        builder strategy.
    """

    def test_match(self):
        """ Match plain route strategy.
        """
        from wheezy.routing.builders import try_build_plain_route
        from wheezy.routing.route import PlainRoute

        r = try_build_plain_route(r'abc')
        assert isinstance(r, PlainRoute)
        assert not r.kwargs

    def test_match_empty(self):
        """ Match plain route strategy.
        """
        from wheezy.routing.builders import try_build_plain_route
        from wheezy.routing.route import PlainRoute

        r = try_build_plain_route(r'')
        assert isinstance(r, PlainRoute)
        assert not r.kwargs

    def test_kwards(self):
        """ Test whenever route is initialized with
            ``kwargs``.
        """
        from wheezy.routing.builders import try_build_plain_route

        r = try_build_plain_route(r'abc', {'a': 1})

        self.assertEqual({'a': 1}, r.kwargs)

    def test_no_match(self):
        """ No match for plain route strategy.
        """
        from wheezy.routing.builders import try_build_plain_route

        r = try_build_plain_route(r'abc/{name}')

        assert r is None


class TryBuildRegexRouteTestCase(unittest.TestCase):
    """ Test the ``builders.try_build_regex_route``.
    """

    def test_instance(self):
        """ Always return an instance of RegexRoute.
        """
        from wheezy.routing.builders import try_build_regex_route
        from wheezy.routing.route import RegexRoute

        r = try_build_regex_route(r'abc')
        assert isinstance(r, RegexRoute)


class BuildRouteTestCase(unittest.TestCase):
    """ Test the ``builders.build_route``
        strategy selection chain of responsibility.
    """

    def test_pattern_is_route(self):
        """ ``pattern`` is an object drived from Route.
        """
        from wheezy.routing.builders import build_route
        from wheezy.routing.route import Route

        r = Route()

        self.assertEqual(r, build_route(r, None, None))

    def test_found(self):
        """ Sutable route strategy has been found.
        """
        from wheezy.routing.builders import build_route
        from wheezy.routing import config

        r = build_route(r'abc', {'a': 1}, config.route_builders)

        assert r
        self.assertEqual({'a': 1}, r.kwargs)

    def test_first_matched(self):
        """ First matched strategy is selected.
        """
        from wheezy.routing.builders import build_route

        m = Mocker()
        mock = m.mock
        builders = mock(), mock(), mock(), mock(), mock()
        b1, b2, b3, b4, b5 = builders
        expect(b1(r'abc', None)).result(None)
        expect(b2(r'abc', None)).result(None)
        expect(b3(r'abc', None)).result('x')
        m.replay()

        r = build_route(r'abc', None, builders)

        self.assertEqual('x', r)
        m.verify()

    def test_not_found(self):
        """ None of available route builders matched
            pattern.
        """
        from wheezy.routing.builders import build_route

        m = Mocker()
        mock = m.mock
        builders = mock(), mock()
        b1, b2 = builders
        expect(b1(r'abc', None)).result(None)
        expect(b2(r'abc', None)).result(None)
        m.replay()

        self.assertRaises(LookupError,
                lambda: build_route(r'abc', None, builders))
        m.verify()


class BuildRouteIntegrationTestCase(unittest.TestCase):
    """ Test integration with ``config.route_builders``.
    """

    def test_match_plain_route(self):
        """ the chain of strategies match plain route.
        """
        from wheezy.routing import config
        from wheezy.routing.builders import build_route
        from wheezy.routing.route import PlainRoute

        r = build_route(r'abc', None,  config.route_builders)

        assert isinstance(r, PlainRoute)

    def test_match_regex_route(self):
        """ the chain of strategies match regex route.
        """
        from wheezy.routing import config
        from wheezy.routing.builders import build_route
        from wheezy.routing.route import RegexRoute

        r = build_route(
                r'abc/(?P<id>\d+)',
                None,
                config.route_builders
        )

        assert isinstance(r, RegexRoute)
