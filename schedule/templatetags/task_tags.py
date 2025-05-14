from django import template

register = template.Library()


@register.simple_tag
def dict_get(d, key):
    return d.get(key)