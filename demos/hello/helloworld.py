
""" ``helloworld`` module.
"""

import sys

from wheezy.routing import PathRouter

if sys.version_info[0] >= 3:
    ntob = lambda n, encoding: n.encode(encoding)
else:
    ntob = lambda n, encoding: n


def hello_world(environ, start_response):
    start_response('200 OK', [
        ('Content-Type', 'text/html')
    ])
    yield ntob('Hello World!', 'utf-8')


def not_found(environ, start_response):
    start_response('404 Not Found', [
        ('Content-Type', 'text/html')
    ])
    yield ntob('', 'utf-8')


r = PathRouter()
r.add_routes([
    ('/', hello_world),
    ('/{any}', not_found)
])


def main(environ, start_response):
    handler, kwargs = r.match(environ['PATH_INFO'])
    return handler(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
