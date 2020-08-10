""" Unit tests for ``helloworld`` module.
"""

import unittest


class MainTestCase(unittest.TestCase):
    """ Test the ``main`` funcation call.
    """

    def test_hello_match(self):
        """
        """
        from helloworld import main

        def start_response(status, response_headers):
            self.assertEquals("200 OK", status)

        environ = {"PATH_INFO": "/"}
        response = list(
            map(lambda c: c.decode("utf-8"), main(environ, start_response))
        )

        self.assertEquals(["Hello World!"], response)

    def test_any_path_match(self):
        """
        """
        from helloworld import main

        def start_response(status, response_headers):
            self.assertEquals("404 Not Found", status)

        for path in ("/a", "/b"):
            environ = {"PATH_INFO": path}
            response = list(
                map(lambda c: c.decode("utf-8"), main(environ, start_response))
            )

            self.assertEquals([""], response)
