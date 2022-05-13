"""
Итак, мы в простейшем варианте реализовали логику PC.
Теперь мы можем создавать новый слой контроллера (новую «вьюшку»), и он абсолютно независим от Application.
"""

from wsgiref.simple_server import make_server


def index_view():
    return '200 OK', [b'Index']


def abc_view():
    return '200 OK', [b'ABC']


def not_found_404_view():
    return '404 WHAT', [b'404 PAGE Not Found']


"""
Здесь мы можем легко сделать «вьюшку» и на базе объекта класса 
(как и функция он с перегрузкой метода __call__() имеет статус callable-объекта и может быть вызван)
"""


class Other:
    # обязательно должен быть __call__ для вызова
    def __call__(self):
        return '200 OK', [b'other']


routes = {
    '/': index_view,
    '/abc/': abc_view,
    '/other/': Other()  # создаем объект класса для вызова
}


class Application:

    def __init__(self, routes):
        self.routes = routes

    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        if path in self.routes:
            view = self.routes[path]
        else:
            view = not_found_404_view
        code, body = view()
        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes)

with make_server('', 8000, application) as httpd:
    print("Serving on port 8000...")
    httpd.serve_forever()
