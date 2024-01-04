from django import template
from gumfuel.models import Category

register = template.Library()  # декоратор для функций


# Функция которая будет возвращвть все категории

@register.simple_tag()  # Декоратером сказали что фунцию можно вызывать в любом html файле
def get_categories():
    return Category.objects.all()


# @register.simple_tag()
# def show_all_tags():
#     return BodyPart.objects.all()


# @register.inclusion_tag('gumfuel_page/list_tags.html')
# def show_all_tags():
#     return {'tags': BodyPart.objects.all()}
