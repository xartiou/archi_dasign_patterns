from wsgiref.simple_server import make_server


# нужно переместить во views
def index_view():
    return '200 OK', [b'Index']


def abc_view():
    return '200 OK', [b'ABC']


def not_found_404_view():
    return '404 WHAT', [b'404 PAGE Not Found']

# нужно переместить в urls
routes = {
    '/': index_view,
    '/abc/': abc_view,
}

# заготовка фреймворка должна быть в отдельном файле
class Application:

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        # Будем проверять, есть ли указанный путь в routes
        # извлекаем из словаря соответствующую функцию и вызываем ее
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return body


# запускающий файл run
application = Application(routes)

with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
