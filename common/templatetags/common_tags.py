from django import template


register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)



@register.filter
def get_keys(dictionaries):
    for dictionary in dictionaries:
        for key in dictionary:
            yield key
            break