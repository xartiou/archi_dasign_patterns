# Начнем издалека.	Для начала поговорим об абстрактных классах.
# В базовом классе Figure метод определяется, в наследниках – переопределяется.

class Figure:
    def draw(self):
        pass


class Circle(Figure):
    def draw(self):
        print('circle')


class Triangle(Figure):
    def draw(self):
        print('triangle')
