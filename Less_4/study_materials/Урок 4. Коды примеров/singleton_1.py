from copy import deepcopy


class Origin:
    pass


o1 = Origin()
o2 = Origin()
o3 = Origin()

print(o1)
print(o2)
print()

# оператор is проверяет идентичность самих объектов.
# Его используют, чтобы удостовериться, что переменные указывают на один и тот же объект в памяти

print(o1 is o2)

a = []
b = a
print(a is b)

b = a.copy()
print(a is b)

b = deepcopy(a)
print(a is b)
