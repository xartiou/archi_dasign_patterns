from wsgiref.simple_server import make_server
"""Для запуска используем wsgiref"""


# заготовка фреймворка
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello world from a simple WSGI application!']


# заготовка запускаемого файла
with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
