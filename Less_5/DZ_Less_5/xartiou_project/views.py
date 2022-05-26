from datetime import date

from xartiou_framework.templator import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import AppRoute, Debug


site = Engine()
logger = Logger('main')

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

            old_watch = site.get_course(name)
            if old_watch:
                new_name = f'copy_{name}'
                new_watch = old_watch.clone()
                new_watch.name = new_name
                site.watches.append(new_watch)

            return '200 OK', render('watch_list.html',
                                    objects_list=site.courses,
                                    name=new_watch.category.name)
        except KeyError:
            return '200 OK', 'No watches have been added yet'
