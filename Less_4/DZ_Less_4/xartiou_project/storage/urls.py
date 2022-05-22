
from storage.views import Index, About, Contacts, PageNotExists, \
    WatchTimetables, WatchesList, CreateWatch, CreateCategory, CategoryList, CopyWatch

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/404/': PageNotExists(),
    '/watch-timetables/': WatchTimetables(),
    '/watch-list/': WatchesList(),
    '/create-watch/': CreateWatch(),
    '/create-category/': CreateCategory(),
    '/category-list/': CategoryList(),
    '/copy-watch/': CopyWatch()
}
