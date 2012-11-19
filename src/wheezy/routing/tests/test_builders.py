
""" Unit tests for ``wheezy.routing.builders``.
"""

import unittest

from mock import Mock


class BuildersTestCase(unittest.TestCase):

    def test_name_raises_error(self):
        """ Name for intermediate route has no sense.
        """
        from wheezy.routing.builders import build_route
        self.assertRaises(AssertionError, lambda: build_route(
            '', finishing=False, kwargs={}, name='wrong', route_builders=None))

    def test_first_match(self):
        """ First route builder match is returned.
        """
        from wheezy.routing.builders import build_route
        mock_builders = [Mock(), Mock(), Mock()]
        mock_builders[0].return_value = None
        mock_builders[1].return_value = 'route'
        assert 'route' == build_route('pattern', finishing=False, kwargs={},
                                      name=None, route_builders=mock_builders)
        mock_builders[0].assert_called_once_with('pattern', False, {}, None)
        mock_builders[1].assert_called_once_with('pattern', False, {}, None)
        assert not mock_builders[2].called

    def test_no_match(self):
        """ If no match found raise error.
        """
        from wheezy.routing.builders import build_route
        self.assertRaises(LookupError, lambda: build_route(
            '', False, {}, None, []))
