from jsonpickle import dumps, loads
from xartiou_framework.templator import render


# поведенческий паттерн - наблюдатель
# Корабль
class Observer:

    def update(self, subject):
        pass


# объект наблюдения
class Subject:

    def __init__(self):
        self.observers = []

    # обходим всех и оповещаем
    def notify(self):
        for item in self.observers:
            item.update(self)


# наблюдатель сообщает по смс
class SmsNotifier(Observer):

    def update(self, subject):
        print('SMS->', 'к нам присоединился', subject.watchmans[-1].name)


# наблюдатель уведомляет через емайл
class EmailNotifier(Observer):

    def update(self, subject):
        print(('EMAIL->', 'к нам присоединился', subject.watchmans[-1].name))


# выполняет сериализацию  и десериализацию объектов
class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    @staticmethod
    def load(data):
        return loads(data)


# поведенческий паттерн - Шаблонный метод
class TemplateView:
    template_name = 'template.html'

    # получаем контекст
    def get_context_data(self):
        return {}

    # получаем шаблон
    def get_template(self):
        return self.template_name

    # передаем контекст в шаблон и рендерим
    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context = {context_object_name: queryset}
        return context


# получаем данные из POST запроса и на их основе создаем новый объект
class CreateView(TemplateView):
    template_name = 'create.html'

    @staticmethod
    def get_request_data(request):
        return request['data']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        else:
            return super().__call__(request)


# поведенческий паттерн - Стратегия
class ConsoleWriter:

    def write(self, text):
        print(text)


class FileWriter:

    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, 'a', encoding='utf-8') as f:
            f.write(f'{text}\n')

