from django import template
from django.urls import reverse, reverse_lazy

register = template.Library()


@register.simple_tag()
def navigation_links():
    return {
        'nav_links1': [
            {'url': reverse('main:about'), 'name': 'About', 'url_name': '/about/'},
            {'url': reverse_lazy('users:profile'), 'name': 'Profile', 'url_name': '/users/profile/'},
        ],
        'nav_links2': [
            {'url': reverse('users:schedule'), 'name': 'Schedule', 'url_name': '/users/schedule/'},
            {'url': '#', 'name': 'Analysis', 'url_name': '/analysis/'},
        ]

    }
