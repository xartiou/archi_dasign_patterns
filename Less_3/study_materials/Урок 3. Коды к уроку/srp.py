# bad
# нарушается принцип SRP, ведь класс делает слишком много. И делает то, что он делать не должен – save, load.
class Order:
    def get_items(self):
        pass

    def get_total(self):
        pass

    def validate(self):
        pass

    def save(self):
        pass

    def load(self):
        pass

# ________________________________________________________________________
#  Предлагается разделить класс на два: GoodOrder и OrderRepository.
# good


class GoodOrder:
    def get_items(self):
        pass

    def get_total(self):
        pass

    def validate(self):
        pass


class OrderRepository:
    def save(self):
        pass

    def load(self):
        pass
