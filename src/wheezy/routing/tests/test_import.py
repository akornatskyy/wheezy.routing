
""" Unit tests for ``wheezy.routing.__init__``.
"""

import unittest


class RoutingPackageImportTestCase(unittest.TestCase):
    """ Test the ``wheezy.routing`` package imports.
    """

    def test_import(self):
        """ Check what can be imported.
        """
        from wheezy import routing

        from inspect import ismodule

        x = [x for x in dir(routing) if x[:2] != '__'
                and not ismodule(eval('routing.' + x))]

        self.assertEqual(['Router', 'url'], x)
