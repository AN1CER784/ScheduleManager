from django.utils import timezone

def combine_date_and_time(date,time):
    if not date or not time:
        return None
    datetime = timezone.make_aware(
        timezone.datetime.combine(date, time),
        timezone.get_current_timezone())
    return datetime

