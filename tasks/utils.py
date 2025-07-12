from datetime import date, time

from django.utils import timezone


def combine_date_and_time(date_value: date, time_value: time):
    if not date_value or not time_value:
        return None
    datetime = timezone.make_aware(
        timezone.datetime.combine(date_value, time_value),
        timezone.get_current_timezone())
    return datetime
