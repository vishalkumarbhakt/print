from wsgiref.simple_server import make_server

class SimpleApp:
    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/plain')])
        return [b'Hello, WSGI World!']

if __name__ == '__main__':
    server = make_server('localhost', 8000, SimpleApp())
    print('Serving on http://localhost:8000/')
    server.serve_forever()