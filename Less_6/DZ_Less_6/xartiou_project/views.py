from datetime import date

from xartiou_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug
from patterns.behavioral_patterns import SmsNotifier, EmailNotifier, \
    ListView, CreateView, BaseSerializer, ConsoleWriter, FileWriter

site = Engine()
logger = Logger('main')
sms_notifier = SmsNotifier()
email_notifier = EmailNotifier


routes = {}


# контроллер - главная страница
@AppRoute(routes=routes, url='/')
class Index:
    @Debug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# контроллер "О проекте"
@AppRoute(routes=routes, url='/about/')
class About:
    @Debug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


# контроллер - Вахты на корабле
@AppRoute(routes=routes, url='/watch-timetables/')
class WatchTimetables:
    @Debug(name='WatchTimetables')
    def __call__(self, request):
        return '200 OK', render('watch_timetables.html', data=date.today())


# контроллер 404
class NotFound404:
    @Debug(name='NotFound404')
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список вахт
@AppRoute(routes=routes, url='/watches-list/')
class WatchesList:
    def __call__(self, request):
        logger.log('Список вахт')
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('watch_list.html',
                                    objects_list=category.watches,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No watches have been added yet'


# контроллер - создать вахту
@AppRoute(routes=routes, url='/create-watch/')
class CreateWatch:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                watch = site.create_watch('record', name, category)

                watch.observers.append(sms_notifier)
                watch.observers.append(email_notifier)

                site.watches.append(watch)

            return '200 OK', render('watch_list.html',
                                    objects_list=category.watches,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_watch.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


# контроллер - список категорий
@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-watch/')
# контроллер - копировать вахту
class CopyWatch:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_watch = site.get_watch(name)
            if old_watch:
                new_name = f'copy_{name}'
                new_watch = old_watch.clone()
                new_watch.name = new_name
                site.watches.append(new_watch)

            return '200 OK', render('watch_list.html',
                                    objects_list=site.watches,
                                    name=new_watch.category.name)
        except KeyError:
            return '200 OK', 'No watches have been added yet'


#  список вахтенных
@AppRoute(routes=routes, url='/watchman-list/')
class WatchmanListView(ListView):
    queryset = site.watchmans
    template_name = 'watchman_list.html'


# создание вахтенного
@AppRoute(routes=routes, url='/create-watchman/')
class WatchmanCreateView(CreateView):
    template_name = 'create_watchman.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('watchman', name)
        site.watchmans.append(new_obj)


# добавление вахтенного на вахту
@AppRoute(routes=routes, url='/add-watchman/')
class AddWatchmanByWatchCreateView(CreateView):
    template_name = 'add_watchman.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['watches'] = site.watches
        context['watchmans'] = site.watchmans
        return context

    def create_obj(self, data: dict):
        watch_name = data['watch_name']
        watch_name = site.decode_value(watch_name)
        watch = site.get_watch(watch_name)
        watchman_name = data['watchman_name']
        watchman_name = site.decode_value(watchman_name)
        watchman = site.get_watchman(watchman_name)
        watch.add_watchman(watchman)


# при получении url='/api/' запаковываем список объектов
@AppRoute(routes=routes, url='/api/')
class WatchApi:
    @Debug(name='WatchApi')
    def __call__(self, request):
        return '200 OK', BaseSerializer(site.watches).save()
