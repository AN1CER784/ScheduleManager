from main.models import Page


def get_page(page_name):
    return Page.objects.get(key=page_name)