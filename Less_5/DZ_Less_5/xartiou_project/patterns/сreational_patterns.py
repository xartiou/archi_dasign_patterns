import copy
import quopri


# абстрактный пользователь
class User:
    pass


# офицер
class Officer(User):
    pass


# вахтеный
class Watchman(User):
    pass


# порождающий паттерн Абстрактная фабрика - фабрика пользователей
class UserFactory:
    types = {
        'watchman': Watchman,
        'officer': Officer
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


# порождающий паттерн Прототип - Курс
class WatchPrototype:
    # прототип вахт корабля

    def clone(self):
        return copy.deepcopy(self)


class Watch(WatchPrototype):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.watches.append(self)


# Морская вахта
class SeeWatch(Watch):
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
        'seewatch': SeeWatch,
        'portwatch': PortWatch
    }

    # порождающий паттерн Фабричный метод
    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


# Основной интерфейс проекта
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
        val_decode_str = quopri.decodestring(val_b)
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
