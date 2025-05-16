from datetime import timedelta

from django import template

register = template.Library()


@register.simple_tag
def subtract_seven_days(date):
    return date - timedelta(days=7)