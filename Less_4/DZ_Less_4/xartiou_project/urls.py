from datetime import date
from views import Index, About, Contacts, WatchTimetables, WatchesList, CreateWatch, CreateCategory, \
    CategoryList, CopyWatch


# front controller
def secret_front(request):
    request['date'] = date.today()


def other_front(request):
    request['key'] = 'key'


fronts = [secret_front, other_front]

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/watch-timetables/': WatchTimetables(),
    '/watch-list/': WatchesList(),
    '/create-watch/': CreateWatch(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-watch/': CopyWatch()
}
