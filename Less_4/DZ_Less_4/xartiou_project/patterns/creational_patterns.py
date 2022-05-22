from copy import deepcopy
from quopri import decodestring


# абстрактный пользователь
class User:
    pass


# командир БЧ
class Officer(User):
    pass


# вахтенный
class Watchman(User):
    pass


class UserFactory:
    types = {
        'watchman': Watchman,
        'officer': Officer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип
class WatchPrototype:
    # прототип вахт корабля

    def clone(self):
        return deepcopy(self)


class Watch(WatchPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.watches.append(self)


# Морская вахта
class SeaWatch(Watch):
    pass


# Общекорабельная Вахта
class GeneralshipWatch(Watch):
    pass


class WatchFactory:
    types = {
        'seawatch': SeaWatch,
        'generalshipwatch': GeneralshipWatch
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# категория
class Category:
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


# основной интерфейс проекта
class Engine:
    def __init__(self):
        self.officer = []
        self.watchman = []
        self.watches = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

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

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        print('log--->', text)
