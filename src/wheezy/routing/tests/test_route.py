
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
        """ ``pattern`` does not end with ``/``.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc')

        assert r.equals_match == r.match


    def test_startswith(self):
        """ ``pattern`` ends with ``/``.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/')

        assert r.startswith_match == r.match


    def test_arguments(self):
        """ The inner state is properly initialized.
        """
        from wheezy.routing.route import PlainRoute

        kw = {'a': 1}
        r = PlainRoute(r'abc', kw)

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
        r = PlainRoute(r'abc', kw)

        matched, kwargs = r.equals_match(r'abc')
        self.assertEquals(3, matched)
        self.assertEquals({'a': 1}, r.kwargs)
        assert kw is not kwargs


    def test_no_kwargs(self):
        """ ``equals_match`` strategy when no kwargs supplied.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc')
        matched, kwargs = r.equals_match(r'abc')
        self.assertEquals(3, matched)
        self.assertEquals(None, r.kwargs)


    def test_no_match(self):
        """ ``equals_match`` strategy when there is no match.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc')
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
        r = PlainRoute(r'abc/', kw)
        matched, kwargs = r.startswith_match(r'abc/de')
        self.assertEquals(4, matched)
        self.assertEquals(kw, kwargs)
        assert kw is not kwargs

    def test_no_kwargs(self):
        """ ``startswith_match`` strategy when no 
            kwargs supplied.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/')
        matched, kwargs = r.startswith_match(r'abc/de')
        self.assertEquals(4, matched)
        self.assertEquals(None, r.kwargs)


    def test_no_match(self):
        """ ``startswith_match`` strategy when there 
            is no match.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/')
        matched, kwargs = r.equals_match(r'ab')
        self.assertEquals(-1, matched)


class PlainRoutePathTestCase(unittest.TestCase):
    """ Test the ``PlainRoute.path``.
    """

    def test_path(self):
        """ Simply return ``pattern``.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/')
        p =  r.path()
        self.assertEquals(p, r.pattern)


    def test_values_ignored(self):
        """ Simply return ``pattern``.
        """
        from wheezy.routing.route import PlainRoute

        r = PlainRoute(r'abc/', {'a': 1})
        p =  r.path({'b': 2})
        self.assertEquals(p, r.pattern)



