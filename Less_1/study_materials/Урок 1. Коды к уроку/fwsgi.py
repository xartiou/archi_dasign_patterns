def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'Hello world from a simple WSGI application!']

# запуск
# uwsgi --http :8000 --wsgi-file fwsgi.py