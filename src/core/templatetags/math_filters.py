from django import template

register = template.Library()


@register.filter
def divide(value):
    return value / 1.91
