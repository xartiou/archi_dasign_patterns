from wsgiref.simple_server import make_server

from xartiou_framework.main import Framework
from urls import fronts
from views import routes


application = Framework(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("Запуск на порту 8080...(http://127.0.0.1:8080/)")
    httpd.serve_forever()
