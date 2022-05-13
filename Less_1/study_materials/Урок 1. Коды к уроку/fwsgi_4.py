"""
Теперь нам нужно реализовать фреймворк так, чтобы можно было писать модели отдельно, вьюшки отдельно,
url-привязки, шаблоны отдельно и т.д.
"""

from wsgiref.simple_server import make_server


""" page controller """


#  делаем отдельно вьюшки
def index_view(request):
    print(request)
    # возвращаем тело ответа в виде списка из bite
    return '200 OK', [b'Index']


def abc_view(request):
    print(request)
    return '200 OK', [b'ABC']


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 PAGE Not Found']


# Теперь у нас есть вьюшки И привязки их к адресам
routes = {
    '/': index_view,
    '/abc/': abc_view,
}


def application(environ, start_response):
    path = environ['PATH_INFO']
    if path == '/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Index']
    elif path == '/abc/':
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'ABC']
    else:
        start_response('404 Not Found', [('Content-Type', 'text/html')])
        return [b'404 Not Found']


with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
