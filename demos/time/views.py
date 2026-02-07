from datetime import datetime

from config import router as r


def welcome(environ, start_response):
    start_response("200 OK", [("Content-type", "text/html")])
    return ["Welcome!  <a href='%s'>Server Time</a>" % r.path_for("now")]


def server_time(environ, start_response):
    start_response("200 OK", [("Content-type", "text/plain")])
    return ["The server time is: %s" % datetime.now()]


def not_found(environ, start_response):
    start_response("404 Not Found", [("Content-Type", "text/plain")])
    return ["Not Found: " + environ["routing.kwargs"]["url"]]
