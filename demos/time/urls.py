
""" ``urls`` module.
"""

from config import url
from views import welcome, server_time, not_found

server_urls = [
    url('time', server_time, name='now')
]

home = [
    ('', welcome),
    ('server/', server_urls)
]

home += [
    url('{url:any}', not_found)
]
