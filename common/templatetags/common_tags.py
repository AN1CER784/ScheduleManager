from pprint import pprint
from typing import TypeVar

from django import template

register = template.Library()

K = TypeVar("K")
V = TypeVar("V")


@register.filter
def get_item(dictionary: dict[K, V], key: K) -> V | None:
    return dictionary.get(key)


@register.filter
def get_values(dictionaries: list[dict]):
    for dictionary in dictionaries:
        for value in dictionary.values():
            yield value
            break
