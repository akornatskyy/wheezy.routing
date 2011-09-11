
""" ``helloworld`` module.
"""

from wheezy.routing import Router


def hello_world(environ, start_response):
    start_response('200 OK', [
        ('Content-type', 'text/html')
    ])
    return ["Hello World!".encode('utf8')]


r = Router()
r.add_routes([
    ('/', hello_world)
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
