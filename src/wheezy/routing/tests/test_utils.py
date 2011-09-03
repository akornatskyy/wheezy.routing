
""" Unit tests for ``wheezy.routing.utils``.
"""

import unittest

from mocker import Mocker, expect


class RouteNameTestCase(unittest.TestCase):
    """ Test the ``route_name`` function.
    """

    def setUp(self):
        self.m = Mocker()

    def tearDown(self):
        self.m.restore()
        self.m.verify()

    def test_class(self):
        """ ``handler`` can be a class.
        """
        from wheezy.routing.utils import route_name

        MockClass = self.m.mock()
        expect(MockClass.__name__).result('MockClass')
        self.m.replay()

        self.assertEquals('mock_class', route_name(MockClass))

    def test_instance(self):
        """ ``handler`` can be an instance.
        """
        from wheezy.routing.utils import route_name

        self.assertEquals('route_name_test_case', route_name(self))

    def test_callable(self):
        """ ``handler`` can be a class.
        """
        from wheezy.routing.utils import route_name

        def my_view():
            pass

        my_view()
        self.assertEquals('my_view', route_name(my_view))

    def test_strip_name(self):
        """ Ensure call to ``strip_name`` function.
        """
        from wheezy.routing.utils import route_name
        from wheezy.routing import utils

        mock_strip_name = self.m.replace(utils.strip_name)
        expect(mock_strip_name('TestCase')).result('TestCase')
        self.m.replay()

        self.assertEquals('test_case', route_name(unittest.TestCase))

    def test_camelcase_to_underscore(self):
        """ Ensure call to ``camelcase_to_underscore`` function.
        """
        from wheezy.routing.utils import route_name
        from wheezy.routing import utils

        MockClass = self.m.mock()
        mock_cc = self.m.replace(utils.camelcase_to_underscore)
        expect(MockClass.__name__).result('TestHandler')
        expect(mock_cc('Test')).result('Test')
        self.m.replay()

        self.assertEquals('Test', route_name(MockClass))


class StripNameTestCase(unittest.TestCase):
    """ Test the ``strip_name`` function.
    """

    def test_match(self):
        """ The ``name`` ends with a word that need to be removed.
        """
        import re

        from wheezy.routing.utils import strip_name
        from wheezy.routing.utils import RE_STRIP_NAME as RE

        suffixes = re.match(
            '\((.*)\)\$', RE.pattern
        ).group(1).split('|')

        for suffix in suffixes:
            self.assertEqual('Login', strip_name('Login' + suffix))

    def test_no_match(self):
        """ The ``name`` is returned unchanged if it doesn't
            contain a word from remove list.
        """
        from wheezy.routing.utils import strip_name

        self.assertEqual('Login', strip_name('Login'))


class CamelCaseToUnderscoreTestCase(unittest.TestCase):
    """ Test the ``camelcase_to_underscore`` function.
    """

    def test_camel_case(self):
        """ The input is a camel case string.
        """
        from wheezy.routing.utils import camelcase_to_underscore

        self.assertEqual(
            'camel_case_to_underscore_test_case',
            camelcase_to_underscore(self.__class__.__name__)
        )

    def test_underscore(self):
        """ The input is with underscore.
        """
        from wheezy.routing.utils import camelcase_to_underscore

        self.assertEqual(
            '__test_case', camelcase_to_underscore('_TestCase')
        )
        self.assertEqual(
            'test_case', camelcase_to_underscore('Test_case')
        )
        self.assertEqual(
            'test__case', camelcase_to_underscore('Test_Case')
        )

    def test_digits(self):
        """ The input contains digits.
        """
        from wheezy.routing.utils import camelcase_to_underscore

        self.assertEqual(
            'test2_case', camelcase_to_underscore('Test2Case')
        )
        self.assertEqual(
            'test_case2', camelcase_to_underscore('TestCase2')
        )
        self.assertEqual(
            'test2_case', camelcase_to_underscore('test2Case')
        )

    def test_abbreviation(self):
        """ The input contains abbreviation.
        """
        from wheezy.routing.utils import camelcase_to_underscore

        self.assertEqual(
            'abc_case', camelcase_to_underscore('ABCCase')
        )
        self.assertEqual(
            'test_abc', camelcase_to_underscore('TestABC')
        )
        self.assertEqual(
            'test2_abc', camelcase_to_underscore('test2ABC')
        )
