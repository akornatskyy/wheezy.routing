
""" ``app`` module.
"""

import config
import urls

r = config.router
r.add_routes(urls.home)


def main(environ, start_response):
    handler, kwargs = r.match(environ['PATH_INFO'][1:])
    environ['routing.kwargs'] = kwargs
    return map(lambda chunk: chunk.encode('utf8'),
            handler(environ, start_response))

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    try:
        print('Visit http://localhost:8080/')
        make_server('', 8080, main).serve_forever()
    except KeyboardInterrupt:
        pass
    print('\nThanks!')
