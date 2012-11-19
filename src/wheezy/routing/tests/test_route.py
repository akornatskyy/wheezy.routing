
""" Unit test for ``wheezy.routing.route``.
"""

import unittest


class RouteTestCase(unittest.TestCase):

    def test_raises_errors(self):
        """ Ensure Route raises errors.
        """
        from wheezy.routing.route import Route
        r = Route()
        assert not r.exact_matches
        self.assertRaises(NotImplementedError, lambda: r.match(''))
        self.assertRaises(NotImplementedError, lambda: r.path())
