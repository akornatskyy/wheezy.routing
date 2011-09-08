
""" Unit test for ``wheezy.routing.router``.
"""

import unittest

from mocker import Mocker, expect


class UrlTestCase(unittest.TestCase):
    """ Test the ``url`` function.
    """

    def test_two_args(self):
        """ A call with two arguments.
        """
        from wheezy.routing.router import url

        u = url('abc', 'handler')

        self.assertEquals(('abc', 'handler', None, None), u)

    def test_three_args(self):
        """ A call with three arguments.
        """
        from wheezy.routing.router import url

        u = url('abc', 'handler', {'id': 1})
        self.assertEquals(('abc', 'handler', {'id': 1}, None), u)

        u = url('abc', 'handler', kwargs={'id': 1})
        self.assertEquals(('abc', 'handler', {'id': 1}, None), u)

        u = url('abc', 'handler', name='name')
        self.assertEquals(('abc', 'handler', None, 'name'), u)

    def test_four_args(self):
        """ A call with four arguments.
        """
        from wheezy.routing.router import url

        u = url('abc', 'handler', {'id': 1}, 'name')
        self.assertEquals(('abc', 'handler', {'id': 1}, 'name'), u)

        u = url('abc', 'handler', kwargs={'id': 1}, name='name')
        self.assertEquals(('abc', 'handler', {'id': 1}, 'name'), u)


class PathRouterInitTestCase(unittest.TestCase):
    """ Test the ``PathRouter.__init__``.
    """

    def test_default_route_builders(self):
        """ default route builders.
        """
        from wheezy.routing.router import PathRouter
        from wheezy.routing import config

        r = PathRouter()

        assert isinstance(r.mapping, list)
        assert isinstance(r.route_map, dict)
        assert isinstance(r.routers, list)
        assert r.route_builders is config.route_builders

    def test_init(self):
        """ custom route builders.
        """
        from wheezy.routing.router import PathRouter
        from wheezy.routing import config

        route_builders = ('x')
        r = PathRouter(route_builders)

        assert isinstance(r.mapping, list)
        assert isinstance(r.route_map, dict)
        assert isinstance(r.routers, list)
        assert r.route_builders is route_builders


class PathRouterAddRouteTestCase(unittest.TestCase):
    """ Test the ``PathRouter.add_route``.
    """

    def setUp(self):
        from wheezy.routing.router import PathRouter

        self.m = Mocker()
        self.r = PathRouter()

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_with_default_name(self):
        """ ``name`` is None.
        """
        MockClass = self.m.mock()
        expect(MockClass.__name__).result('MockClass')
        self.m.replay()

        self.r.add_route(r'abc', MockClass)

        assert 'mock_class' in tuple(self.r.route_map.keys())

    def test_with_name(self):
        """ ``name`` is supplied.
        """
        self.r.add_route(r'abc', 'x', name='my_name')

        assert 'my_name' in tuple(self.r.route_map.keys())

    def test_with_default_kwargs(self):
        """ ``kwargs`` is None.
        """
        self.r.add_route(r'abc', 'x', kwargs=None, name='n')

        route = self.r.route_map['n']
        assert route.kwargs is None

    def test_with_kwargs(self):
        """ ``kwargs`` is supplied.
        """
        kw = {'a': 1}
        self.r.add_route(r'abc', 'x', kwargs=kw, name='n')

        route = self.r.route_map['n']
        self.assertEquals(kw, route.kwargs)

    def test_build_route(self):
        """ ``build_route`` call.
        """
        from wheezy.routing import builders

        kw = {'a': 1}
        mock_build_route = self.m.replace(builders.build_route)
        expect(
            mock_build_route('abc', kw, self.r.route_builders)
        ).result('x')
        self.m.replay()

        self.r.add_route('abc', 'x', kwargs=kw, name='n')

    def test_mapping(self):
        """ mapping has route and handler pair
        """
        self.r.add_route(r'abc', 'x', kwargs=None, name='n')

        assert 1 == len(self.r.route_map) == len(self.r.mapping)
        route = self.r.route_map['n']
        mroute, handler = self.r.mapping[0]
        assert route is mroute


class PathRouterIncludeTestCase(unittest.TestCase):
    """ Test the ``PathRouter.include``.
    """

    def setUp(self):
        from wheezy.routing.router import PathRouter

        self.m = Mocker()
        self.r = PathRouter()

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_build_route(self):
        """ ``build_route`` call.
        """
        from wheezy.routing import builders

        kw = {'a': 1}
        mock_build_route = self.m.replace(builders.build_route)
        expect(
            mock_build_route('abc', kw, self.r.route_builders)
        ).result('x')
        self.m.replay()

        self.r.include('abc', [], kwargs=kw)

    def test_inner(self):
        """ init of inner ``PathRouter``.
        """
        from wheezy.routing import router

        mock_router = self.m.proxy(router.PathRouter())
        MockPathRouter = self.m.replace(router.PathRouter)
        expect(
            MockPathRouter(self.r.route_builders)
        ).result(mock_router)
        expect(mock_router.add_routes([])).passthrough()
        self.m.replay()

        self.r.include('abc', [])

        assert mock_router is self.r.routers[0][0]

    def test_routers(self):
        """ reverse mapping between routers and mapping.
        """
        self.r.include('abc', [])

        mr, mi = self.r.mapping[0]
        ri, rr = self.r.routers[0]

        assert mr is rr
        assert mi is ri


class PathRouterAddRoutesTestCase(unittest.TestCase):
    """ Test the ``PathRouter.add_routes``.
    """

    def setUp(self):
        from wheezy.routing.router import PathRouter
        self.m = Mocker()
        self.r = PathRouter()

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_mapping_is_tuple_of_two(self):
        """ ``mapping`` is a tuple of two elements.
        """
        m = [('pattern', 'handler')]
        self.r.add_route = mock_add_route = self.m.mock()
        expect(mock_add_route('pattern', 'handler', None, None))
        self.m.replay()

        self.r.add_routes(m)

    def test_mapping_is_tuple_of_three(self):
        """ ``mapping`` is a tuple of three elements.
        """
        m = [('pattern', 'handler', 'kwargs')]
        self.r.add_route = mock_add_route = self.m.mock()
        expect(
            mock_add_route('pattern', 'handler', 'kwargs', None)
        )
        self.m.replay()

        self.r.add_routes(m)

    def test_mapping_is_tuple_of_four(self):
        """ ``mapping`` is a tuple of four elements.
        """
        m = [('pattern', 'handler', 'kw', 'name')]
        self.r.add_route = mock_add_route = self.m.mock()
        expect(
            mock_add_route('pattern', 'handler', 'kw', 'name')
        )
        self.m.replay()

        self.r.add_routes(m)

    def test_include(self):
        """ ``include`` call.
        """
        from wheezy.routing.router import PathRouter

        r = PathRouter()
        self.r.include = mock_include = self.m.mock()
        for h in ([], (), r):
            expect(mock_include('pattern', h, 'kwargs'))
        self.m.replay()

        for h in ([], (), r):
            m = [('pattern', h, 'kwargs')]
            self.r.add_routes(m)


class PathRouterMatchTestCase(unittest.TestCase):
    """ Test the ``PathRouter.match``.
    """

    def setUp(self):
        from wheezy.routing.router import PathRouter

        self.m = Mocker()
        self.r = PathRouter()

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_no_match(self):
        """ there is no match.
        """
        handler, kwargs = self.r.match('abc')

        assert handler is None
        assert kwargs is None

    def test_matched_is_zero(self):
        """ empty ``path`` is matched.
        """
        from wheezy.routing import builders

        mock_route = self.m.mock()
        mock_build_route = self.m.replace(builders.build_route)
        expect(
            mock_build_route('', None, self.r.route_builders)
        ).result(mock_route)
        expect(mock_route.match('')).result((0, None))
        self.m.replay()

        self.r.add_route('', 1, name='x')
        handler, kwargs = self.r.match('')

        self.assertEquals(1, handler)

    def test_first_match(self):
        """ the first match is taken.
        """
        self.r.add_routes([
            ('abc', 0),
            ('bcd', 1),
            ('bcd', 2)
        ])

        handler, kwargs = self.r.match('bcd')


class PathRouterMatchInnerTestCase(unittest.TestCase):
    """ Test the ``PathRouter.match`` inner router.
    """

    def setUp(self):
        from wheezy.routing import router

        self.m = Mocker()
        self.r = router.PathRouter()
        self.mock_inner = self.m.proxy(router.PathRouter())
        MockPathRouter = self.m.replace(router.PathRouter)
        expect(
            MockPathRouter(self.r.route_builders)
        ).result(self.mock_inner)
        expect(self.mock_inner.add_routes([]))

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_no_match(self):
        """ there is no match.
        """
        expect(self.mock_inner.match('de')).result((None, None))
        self.m.replay()

        self.r.include('abc/', [])
        handler, kwargs = self.r.match('abc/de')

        assert handler is None
        assert kwargs is None

    def test_no_match_continue(self):
        """ there is no match, continue with the rest
            in ``self.mapping``.
        """
        expect(self.mock_inner.match('de')).result((None, None))
        self.m.replay()

        self.r.include('abc/', [])
        self.r.add_route('abc/de', 'h')
        handler, kwargs = self.r.match('abc/de')

        self.assertEquals('h', handler)

    def test_no_kwargs(self):
        """ there is a match is inner, kwargs and kwargs2
            are None.
        """
        expect(self.mock_inner.match('de')).result(('h', None))
        self.m.replay()

        self.r.include('abc/', [])
        handler, kwargs = self.r.match('abc/de')

        self.assertEquals('h', handler)
        assert kwargs is None

    def test_kwargs_outer(self):
        """ there is a match is inner, kwargs in not None
            and kwargs2 is None.
        """
        expect(self.mock_inner.match('de')).result(('h', None))
        self.m.replay()

        kw = {'a': 1}
        self.r.include('abc/', [], kw)
        handler, kwargs = self.r.match('abc/de')

        self.assertEquals('h', handler)
        self.assertEquals(kw, kwargs)
        assert kw is kwargs

    def test_kwargs_inner(self):
        """ there is a match is inner, kwargs is None
            and kwargs2 not None.
        """
        kw = {'a': 1}
        expect(self.mock_inner.match('de')).result(('h', kw))
        self.m.replay()

        self.r.include('abc/', [])
        handler, kwargs = self.r.match('abc/de')

        self.assertEquals('h', handler)
        self.assertEquals(kw, kwargs)

    def test_kwargs_merge(self):
        """ there is a match is inner, kwargs and kwargs2
            are None.
        """
        expect(self.mock_inner.match('de')).result(('h', {'b': 2}))
        self.m.replay()

        self.r.include('abc/', [], {'a': 1})
        handler, kwargs = self.r.match('abc/de')

        self.assertEquals('h', handler)

    def test_merge_inner_override_outer(self):
        """ inner match kwargs override outer kwargs.
        """
        expect(self.mock_inner.match('de')).result(('h',
            {'a': 1000, 'b': 2}))
        self.m.replay()

        self.r.include('abc/', [], {'a': 1})
        handler, kwargs = self.r.match('abc/de')

        self.assertEquals('h', handler)
        self.assertEquals({'a': 1000, 'b': 2}, kwargs)


class PathRouterPathForTestCase(unittest.TestCase):
    """ Test the ``PathRouter.path_for``.
    """

    def setUp(self):
        from wheezy.routing import router

        self.m = Mocker()
        self.r = router.PathRouter()

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_no_match(self):
        """ no match
        """
        path = self.r.path_for('n', a=1)
        self.assertEquals(None, path)

    def test_route_map(self):
        """ the name exists in ``route_map``.
        """
        from wheezy.routing import builders

        mock_route = self.m.mock()
        mock_build_route = self.m.replace(builders.build_route)
        expect(
            mock_build_route('abc', None, self.r.route_builders)
        ).result(mock_route)
        expect(mock_route.path({'a': 1})).result('abc')
        self.m.replay()

        self.r.add_route('abc', 'handler', name='n')
        path = self.r.path_for('n', a=1)

        self.assertEquals('abc', path)


class PathRouterPathForInnerTestCase(unittest.TestCase):
    """ Test the ``PathRouter.path_for`` inner router.
    """

    def setUp(self):
        from wheezy.routing import router

        self.m = Mocker()
        self.r = router.PathRouter()
        self.mock_inner = self.m.proxy(router.PathRouter())
        self.MockPathRouter = self.m.replace(router.PathRouter)
        expect(
            self.MockPathRouter(self.r.route_builders)
        ).result(self.mock_inner)
        expect(self.mock_inner.add_routes([]))

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_no_match(self):
        """ no match
        """
        expect(self.mock_inner.path_for('n')).result(None)
        self.m.replay()

        self.r.include('abc/', [])
        p = self.r.path_for('n')

        assert p is None

    def test_match(self):
        """ match inner router
        """
        expect(self.mock_inner.path_for('n')).result('de')
        self.m.replay()

        self.r.include('abc/', [])
        p = self.r.path_for('n')

        self.assertEquals('abc/de', p)

    def test_match_first(self):
        """ match inner router
        """
        from wheezy.routing import router

        mock_inner2 = self.m.proxy(router.PathRouter())
        expect(
            self.MockPathRouter(self.r.route_builders)
        ).result(mock_inner2)
        expect(mock_inner2.add_routes([]))

        expect(self.mock_inner.path_for('n')).result('de')
        self.m.replay()

        self.r.include('abc/', [])
        self.r.include('cbd/', [])
        p = self.r.path_for('n')

        self.assertEquals('abc/de', p)
