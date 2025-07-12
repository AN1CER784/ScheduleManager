from typing import Literal

from main.models import Page


def get_page(page_name: Literal["main", "about"]) -> Page:
    return Page.objects.get(key=page_name)
