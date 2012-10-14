
""" Unit test for ``wheezy.routing.route``.
"""

import unittest


class RouteTestCase(unittest.TestCase):
    """ Test the ``Route` class.
    """

    def test_init(self):
        """ Route class can be instantiated.
        """
        from wheezy.routing.route import Route

        r = Route()

        assert r

    def test_match_raise_error(self):
        """ ``Route.match`` raises error
        """
        from wheezy.routing.route import Route

        r = Route()
        self.assertRaises(NotImplementedError,
                          lambda: r.match(''))

    def test_path_raise_error(self):
        """ ``Route.match`` raises error
        """
        from wheezy.routing.route import Route

        r = Route()
        self.assertRaises(NotImplementedError,
                          lambda: r.path())


class PlainRouteInitTestCase(unittest.TestCase):
    """ Test the ``PlainRoute.__init__`` class.
    """

    def test_equals(self):
        """ Finishing route.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc', True)

        assert r.equals_match == r.match

    def test_startswith(self):
        """ Intermediate route.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/', False)

        assert r.startswith_match == r.match

    def test_arguments(self):
        """ The inner state is properly initialized.
        """
        from wheezy.routing.route import PlainRoute

        kw = {'a': 1}
        r = PlainRoute(r'abc', True, kw)

        self.assertEquals(r'abc', r.pattern)
        self.assertEquals(kw, r.kwargs)
        self.assertEquals(3, r.matched)
        assert kw is r.kwargs


class PlainRouteEqualsMatchTestCase(unittest.TestCase):
    """ Test the ``PlainRoute.equals_match`` class.
    """

    def test_kwargs(self):
        """ matched
        """
        from wheezy.routing.route import PlainRoute

        kw = {'a': 1}
        r = PlainRoute(r'abc', True, kw)

        matched, kwargs = r.equals_match(r'abc')
        self.assertEquals(3, matched)
        self.assertEquals({'a': 1}, r.kwargs)
        assert kw is kwargs

    def test_no_kwargs(self):
        """ ``equals_match`` strategy when no kwargs supplied.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc', True)
        matched, kwargs = r.equals_match(r'abc')
        self.assertEquals(3, matched)
        self.assertEquals(None, r.kwargs)

    def test_no_match(self):
        """ ``equals_match`` strategy when there is no match.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc', True)
        matched, kwargs = r.equals_match(r'ab')
        self.assertEquals(-1, matched)


class PlainRouteStartswithMatchTestCase(unittest.TestCase):
    """ Test the ``PlainRoute.startswith_match``.
    """

    def test_kwargs(self):
        """ match strategy.
        """
        from wheezy.routing.route import PlainRoute

        kw = {'a': 1}
        r = PlainRoute(r'abc/', False, kw)
        matched, kwargs = r.startswith_match(r'abc/de')
        self.assertEquals(4, matched)
        self.assertEquals(kw, kwargs)
        assert kw is kwargs

    def test_no_kwargs(self):
        """ ``startswith_match`` strategy when no
            kwargs supplied.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/', False)
        matched, kwargs = r.startswith_match(r'abc/de')
        self.assertEquals(4, matched)
        self.assertEquals(None, r.kwargs)

    def test_no_match(self):
        """ ``startswith_match`` strategy when there
            is no match.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/', False)
        matched, kwargs = r.equals_match(r'ab')
        self.assertEquals(-1, matched)


class PlainRoutePathTestCase(unittest.TestCase):
    """ Test the ``PlainRoute.path``.
    """

    def test_path(self):
        """ Simply return ``pattern``.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/', False)
        p = r.path()
        self.assertEquals(p, r.pattern)

    def test_values_ignored(self):
        """ Simply return ``pattern``.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/', True, {'a': 1})
        p = r.path({'b': 2})
        self.assertEquals(p, r.pattern)


class RegexRouteInitTestCase(unittest.TestCase):
    """ Test the ``RegexRoute.__init__``.
    """

    def test_with_kwargs(self):
        """ If kwargs are supplied than choose
            ``match_with_kwargs`` strategy.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', False, {'a': 1})

        assert r.match == r.match_with_kwargs

    def test_no_kwargs(self):
        """ If kwargs omitted than choose
            ``match_no_kwargs`` strategy.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', True)

        assert r.match == r.match_no_kwargs


class RegexRouteMatchNoKwargsPartsTestCase(unittest.TestCase):
    """ Test the ``RegexRoute.match_no_kwargs``.
    """

    def test_no_match_intermediate(self):
        """ there is no match.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', False)
        matched, kwargs = r.match('ab')

        self.assertEquals(-1, matched)
        assert not kwargs

    def test_no_match_finishing(self):
        """ there is no match.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', True)
        matched, kwargs = r.match('abcd')

        self.assertEquals(-1, matched)
        assert not kwargs

    def test_match_intermediate(self):
        """ there is a match.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', False)
        matched, kwargs = r.match('abcd')

        self.assertEquals(3, matched)
        assert not kwargs

    def test_match_finishing(self):
        """ there is a match.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', True)
        matched, kwargs = r.match('abc')

        self.assertEquals(3, matched)
        assert not kwargs


class RegexRouteMatchWithKwargsPartsTestCase(unittest.TestCase):
    """ Test the ``RegexRoute.match_with_kwargs``.
    """

    def test_no_match(self):
        """  there is no match.
        """
        from wheezy.routing.route import RegexRoute

        r = RegexRoute(r'abc', {'a': 1})
        matched, kwargs = r.match('bc')

        self.assertEquals(-1, matched)
        assert not kwargs

    def test_match(self):
        """  there is a match.
        """
        from wheezy.routing.route import RegexRoute

        kw = {'a': 1}
        r = RegexRoute(r'abc', False, kw)
        matched, kwargs = r.match('abcd')

        self.assertEquals(3, matched)
        self.assertEquals(kw, kwargs)
        assert kw is not kwargs

    def test_match_merge(self):
        """ default kwargs are merged with match kwargs.
        """
        from wheezy.routing.route import RegexRoute

        kw = {'a': 1}
        r = RegexRoute(r'abc/(?P<b>\d+)', True, kw)
        matched, kwargs = r.match('abc/2')

        self.assertEquals(5, matched)
        self.assertEquals({'a': 1, 'b': '2'}, kwargs)
        self.assertEquals({'a': 1, 'b': ''}, r.kwargs)


class RegexRoutePathTestCase(unittest.TestCase):
    """ Test the ``RegexRoute.path``.
    """

    def setUp(self):
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(r'abc/(?P<a>\d+)', False)

    def test_no_values(self):
        """
        """
        self.assertRaises(TypeError, lambda: self.r.path())

    def test_with_values(self):
        """
        """
        path = self.r.path(dict(a=2))

        self.assertEquals('abc/2', path)


class RegexRoutePathNoDefaultsTestCase(unittest.TestCase):
    """ Test the ``RegexRoute.path``.
    """

    def setUp(self):
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(r'abc/(?P<a>\d+)', True)

    def test_no_values(self):
        """
        """
        self.assertRaises(TypeError, lambda: self.r.path())

    def test_with_values(self):
        """
        """
        path = self.r.path(dict(a=2))

        self.assertEquals('abc/2', path)


class RegexRoutePathWithDefaultsTestCase(unittest.TestCase):
    """ Test the ``RegexRoute.path``.
    """

    def setUp(self):
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(r'abc/(?P<a>\d+)', True, {'a': 1})

    def test_no_values(self):
        """
        """
        path = self.r.path()

        self.assertEquals('abc/1', path)

    def test_with_values(self):
        """
        """
        path = self.r.path(dict(a=2))

        self.assertEquals('abc/2', path)


class RegexRouteCurlyIntTestCase(unittest.TestCase):
    """ Test the ``RegexRoute`` while initialized
        by curly route builder strategy that uses
        ``curly.convert`` function to build regex
        from curly ``int``  expression.
    """

    def setUp(self):
        from wheezy.routing.curly import convert
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(convert('abc/{id:int}'), True)

    def test_match(self):
        """ match
        """
        matched, kwargs = self.r.match('abc/1234')

        self.assertEquals(8, matched)
        self.assertEquals({'id': '1234'}, kwargs)

    def test_no_match(self):
        """ no match
        """
        matched, kwargs = self.r.match('abc/de')

        self.assertEquals(-1, matched)
        assert kwargs is None

    def test_path(self):
        """
        """
        path = self.r.path(dict(id=1234))

        self.assertEquals('abc/1234', path)


class RegexRouteCurlyWordTestCase(unittest.TestCase):
    """ Test the ``RegexRoute`` while initialized
        by curly route builder strategy that uses
        ``curly.convert`` function to build regex
        from curly ``word`` expression.
    """

    def setUp(self):
        from wheezy.routing.curly import convert
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(convert('abc/{id:word}'), True)

    def test_match(self):
        """ match
        """
        matched, kwargs = self.r.match('abc/de')

        self.assertEquals(6, matched)
        self.assertEquals({'id': 'de'}, kwargs)

    def test_no_match(self):
        """ no match
        """
        matched, kwargs = self.r.match('abc/*e')

        self.assertEquals(-1, matched)
        assert kwargs is None

    def test_path(self):
        """
        """
        path = self.r.path(dict(id=1234))

        self.assertEquals('abc/1234', path)


class RegexRouteCurlySegmentTestCase(unittest.TestCase):
    """ Test the ``RegexRoute`` while initialized
        by curly route builder strategy that uses
        ``curly.convert`` function to build regex
        from curly ``segment`` expression.
    """

    def setUp(self):
        from wheezy.routing.curly import convert
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(convert('abc/{id:segment}'), False)

    def test_match(self):
        """ match
        """
        matched, kwargs = self.r.match('abc/de/f')

        self.assertEquals(6, matched)
        self.assertEquals({'id': 'de'}, kwargs)

    def test_no_match(self):
        """ no match
        """
        matched, kwargs = self.r.match('abc')

        self.assertEquals(-1, matched)
        assert kwargs is None

    def test_path(self):
        """
        """
        path = self.r.path(dict(id=1234))

        self.assertEquals('abc/1234', path)


class RegexRouteCurlyAnyTestCase(unittest.TestCase):
    """ Test the ``RegexRoute`` while initialized
        by curly route builder strategy that uses
        ``curly.convert`` function to build regex
        from curly ``any`` expression.
    """

    def setUp(self):
        from wheezy.routing.curly import convert
        from wheezy.routing.route import RegexRoute

        self.r = RegexRoute(convert('abc/{id:any}'), True)

    def test_match(self):
        """ match
        """
        matched, kwargs = self.r.match('abc/de/f')

        self.assertEquals(8, matched)
        self.assertEquals({'id': 'de/f'}, kwargs)

    def test_no_match(self):
        """ no match
        """
        matched, kwargs = self.r.match('abc')

        self.assertEquals(-1, matched)
        assert kwargs is None

    def test_path(self):
        """
        """
        path = self.r.path(dict(id=1234))

        self.assertEquals('abc/1234', path)
