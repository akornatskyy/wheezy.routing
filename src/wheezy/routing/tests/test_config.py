
""" Unit tests for ``wheezy.routing.config``
""" 

import unittest

class RouteBuildersTestCase(unittest.TestCase):


    def test_builder_callable(self):
        """ Ensure items in ``route_builders`` list are 
            callable(pattern, kwargs=None)
        """
        from wheezy.routing import config

        import inspect

        for builder in config.route_builders:
            assert builder
            assert callable(builder)
            args, varargs, keywords, defaults = \
                    inspect.getargspec(builder)
            self.assertEqual(['pattern', 'kwargs'], args)
            self.assertEqual(None, varargs)
            self.assertEqual(None, keywords)
            self.assertEqual((None,), defaults)

