""" Functional tests for ``time`` applications.
"""

import unittest


class FunctionalTestCase(unittest.TestCase):
    """Functional tests for ``time`` application."""

    def go(self, path, expected_status="200 OK"):
        """Make a call to ``main`` function setting
        wsgi ``environ['PATH_INFO']`` to ``path``
        and validating expected http response
        status.
        """
        from app import main

        def start_response(status, response_headers):
            assert expected_status == status

        environ = {"PATH_INFO": path}
        return "".join(
            map(
                lambda chunk: chunk.decode("utf-8"),
                main(environ, start_response),
            )
        )

    def test_welcome(self):
        """Welcome page must have a valid path
        to ``server_time`` view.
        """
        response = self.go("/")

        assert "Welcome" in response
        assert "href='server/time'" in response

    def test_server_time(self):
        """Ensure it is a server time page."""
        response = self.go("/server/time")

        assert "time is" in response

    def test_not_found(self):
        """Ensure HTTP 404 for requests that has no
        intended request processors (views).
        """
        for path in ("/server", "/server/", "/server/time/x", "/x", "/abc"):
            response = self.go(path, "404 Not Found")

            assert "Not Found" in response
            assert path[1:] in response
