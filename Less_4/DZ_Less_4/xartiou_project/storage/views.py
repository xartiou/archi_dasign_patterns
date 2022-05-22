from datetime import date
from xartiou_framework.templator import render
from patterns.creational_patterns import Engine, Logger


site = Engine()
logger = Logger('main')


# контроллер - главная страница
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', style=request.get('style', None))


# контроллер "О проекте"
class About:
    def __call__(self, request):
        return '200 OK', render('about.html', style=request.get('style', None))


# контроллер "Контакты"
class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', style=request.get('style', None))


# контроллер 404
class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - Расписания вахт
class WatchTimetables:
    def __call__(self, request):
        return '200 OK', render('watch-timetables.html', date=date.today())


# контроллер - список вахт
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
            return '200 OK', 'Вахты еще не добавлены.'


# контроллер - создать вахту
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

            return '200 OK', render('watch-list.html',
                                    objects_list=category.watches,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create-watch.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'Категории еще не добавлены'


# контроллер - создать категорию
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
            return '200 OK', render('create-category.html',
                                    categories=categories)


# контроллер - список категорий
class CategoryList:
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category-list.html',
                                objects_list=site.categories)


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

            return '200 OK', render('watch-list.html',
                                    objects_list=site.watches,
                                    name=new_watch.category.name)
        except KeyError:
            return '200 OK', 'Курсы еще не добавлены'
