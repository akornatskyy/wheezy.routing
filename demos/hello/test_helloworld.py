
""" Unit tests for ``helloworld`` module.
"""

import unittest


class MainTestCase(unittest.TestCase):
    """ Test the ``main`` funcation call.
    """

    def test_any_path_match(self):
        """
        """
        from helloworld import main

        def start_response(status, response_headers):
            pass

        for path in ('/', '/Welcome'):
            environ = {'PATH_INFO': path}
            response = main(environ, start_response)

            self.assertEquals(['Hello World!'], response)
