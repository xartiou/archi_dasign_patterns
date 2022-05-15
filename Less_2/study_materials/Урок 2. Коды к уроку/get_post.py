from wsgiref.simple_server import make_server


def application(environ, start_response):
    method = environ['REQUEST_METHOD']
    print('method', method)  # method GET
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello world from a simple WSGI application!']


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...(http://127.0.0.1:8000/)")
    httpd.serve_forever()
