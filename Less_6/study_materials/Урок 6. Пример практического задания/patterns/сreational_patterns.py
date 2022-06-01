from copy import deepcopy
from quopri import decodestring
from behavioral_patterns import FileWriter, Subject


# абстрактный пользователь
class User:
    def __init__(self, name):
        self.name = name


# Офицер
class Officer(User):
    pass


# вахтенный
class Watchman(User):

    def __init__(self, name):
        self.watches = []
        super().__init__(name)


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'watchman': Watchman,
        'officer': Officer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


# порождающий паттерн Прототип - Вахта
class WatchPrototype:
    # прототип корабельных вахт

    def clone(self):
        return deepcopy(self)


class Watch(WatchPrototype, Subject):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.watches.append(self)
        self.watchmans = []
        super().__init__()

    def __getitem__(self, item):
        return self.watchmans[item]

    def add_student(self, watchman: Watchman):
        self.watchmans.append(watchman)
        watchman.watches.append(self)
        self.notify()


# Морская вахта
class SeaWatch(Watch):
    pass


# Портовая вахта
class PortWatch(Watch):
    pass


# Категория
class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.watches = []

    def watch_count(self):
        result = len(self.watches)
        if self.category:
            result += self.category.watch_count()
        return result


# порождающий паттерн Абстрактная фабрика - фабрика вахт
class WatchFactory:
    types = {
        'seawatch': SeaWatch,
        'portwatch': PortWatch
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной интерфейс проекта
class Engine:
    def __init__(self):
        self.officers = []
        self.watchmans = []
        self.watches = []
        self.categories = []

    @staticmethod
    def create_user(type_, name):
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    @staticmethod
    def create_watch(type_, name, category):
        return WatchFactory.create(type_, name, category)

    def get_watch(self, name):
        for item in self.watches:
            if item.name == name:
                return item
        return None

    def get_watchman(self, name) -> Watchman:
        for item in self.watchmans:
            if item.name == name:
                return item

    @staticmethod
    def decode_value(val):
        val_b = bytes(val.replace('%', '=').replace("+", " "), 'UTF-8')
        val_decode_str = decodestring(val_b)
        return val_decode_str.decode('UTF-8')


# порождающий паттерн Синглтон
class SingletonByName(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=SingletonByName):

    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        text = f'log---> {text}'
        self.writer.write(text)
