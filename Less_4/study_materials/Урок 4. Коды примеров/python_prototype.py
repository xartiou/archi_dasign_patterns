from copy import deepcopy


class Original:
    pass


original = Original()
prototype = deepcopy(original)


prototype.name = 2


# original = Original(1, 2, 3, 4, 5, 6, 7, 7)

"""
class Course:
    pass


obj_1 = Course(1, 2, 3, 4, 5, 6, 7)
obj_1.name = 1

obj_2 = Course(1, 2, 3, 4, 5, 6, 7)
"""


