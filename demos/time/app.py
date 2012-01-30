
""" ``app`` module.
"""

from config import router
from urls import all_urls


router.add_routes(all_urls)


def main(environ, start_response):
    handler, kwargs = router.match(environ['PATH_INFO'].lstrip('/'))
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
