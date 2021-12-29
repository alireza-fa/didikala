from django.db.models import Q, Sum

from catalogue.models import ProductType, Category, Product
from django import template

register = template.Library()


@register.simple_tag
def get_product_type():
    return ProductType.objects.all()


@register.filter
def category_parent(typ):
    return typ.categories.filter(is_child=False)


@register.filter
def category_child(cat):
    children = cat.children.filter(is_child=True)
    if not children.exists():
        return cat.brands.all()
    return children


@register.filter
def negative_three(value):
    return int(value) - 3


def positive_three(value):
    return int(value) + 3


def convert_int(value):
    return int(value)


@register.filter
def times(number):
    return range(number)


@register.simple_tag
def get_products():
    return Product.objects.all()
