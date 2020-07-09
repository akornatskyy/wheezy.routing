""" ``urls`` module.
"""

from views import not_found, server_time, welcome

from wheezy.routing import url

server_urls = [url("time", server_time, name="now")]

all_urls = [("", welcome), ("server/", server_urls)]
all_urls += [url("{url:any}", not_found)]
