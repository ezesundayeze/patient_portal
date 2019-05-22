
from django import template

register = template.Library()

@register.filter
def replace_comma(param):
    return str(param).replace(',', '')

@register.filter
def joinby(value, arg):
    return arg.join(value)


@register.filter(is_safe=True)
def myfilter(value):
    return value