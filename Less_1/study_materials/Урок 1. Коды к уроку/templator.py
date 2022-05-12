"""
Используем шаблонизатор jinja2
"""
from jinja2 import Template


"""
    render() — Объединяет заданный шаблон с заданным контекстным словарем
    и возвращает объект HttpResponse с этим визуализированным кодом
"""


def render(template_name, **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # Открываем шаблон по имени
    with open(template_name, encoding='utf-8') as f:
        # Читаем
        template = Template(f.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)


if __name__ == '__main__':
    # Пример использования
    output_test = render('authors.html',
                         object_list=[{'name': 'Leo'}, {'name': 'Kate'}])
    print(output_test)
