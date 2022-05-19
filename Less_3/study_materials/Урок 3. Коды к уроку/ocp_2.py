# Как бы сделать так, чтобы программа указала нам, что мы забыли переопределить метод draw()?
class Figure:
    def draw(self):
        pass


class Circle(Figure):
    def draw(self):
        print('circle')


class Triangle(Figure):
    def draw(self):
        print('triangle')


class Romb(Figure):
    pass


romb = Romb()
print(romb.draw())
