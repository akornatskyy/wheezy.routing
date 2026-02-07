import inspect
import unittest

from wheezy.routing import config


def callable(obj):
    return any("__call__" in klass.__dict__ for klass in type(obj).__mro__)


class RouteBuildersTestCase(unittest.TestCase):
    """Test the ``config.route_builders`` setting."""

    def test_builder_callable(self):
        """Ensure items in ``route_builders`` list are
        callable(pattern, kwargs=None)
        """
        for builder in config.route_builders:
            assert builder
            assert callable(builder)
            spec = inspect.getfullargspec(builder)
            self.assertEqual(
                ["pattern", "finishing", "kwargs", "name"], spec.args
            )
            self.assertEqual(None, spec.varargs)
            self.assertEqual(None, spec.varkw)
            self.assertEqual((True, None, None), spec.defaults)
