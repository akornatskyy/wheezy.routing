
""" Unit tests for ``wheezy.routing.config``.
"""

import unittest

from wheezy.routing.p2to3 import iscallable


class RouteBuildersTestCase(unittest.TestCase):
    """ Test the ``config.route_builders`` setting.
    """

    def test_builder_callable(self):
        """ Ensure items in ``route_builders`` list are
            callable(pattern, kwargs=None)
        """
        import inspect

        from wheezy.routing import config

        for builder in config.route_builders:
            assert builder
            assert iscallable(builder)
            args, varargs, keywords, defaults = \
                    inspect.getargspec(builder)
            self.assertEqual(['pattern', 'kwargs'], args)
            self.assertEqual(None, varargs)
            self.assertEqual(None, keywords)
            self.assertEqual((None,), defaults)
