from abc import ABC, abstractmethod

# Цель – есть некоторая иерархия объектов и мы хотим не зависеть от конкретики в клиентском коде.


class Animal(ABC):

    @abstractmethod
    def say(self):
        pass

    # определяет интерфейс для создания объектов,
    # при этом выбранный класс инстанцируется подклассами

    @staticmethod
    def create_animal(animal_type):
        ANIMALS = {
            'dog': Dog,
            'cat': Cat,
            'bear': Bear
        }
        return ANIMALS[animal_type]()


class Dog(Animal):

    def say(self):
        print('wow-wow')


class Cat(Animal):

    def say(self):
        print('мяу-мяу')


class Bear(Animal):

    def say(self):
        print('мяу-мяу')
