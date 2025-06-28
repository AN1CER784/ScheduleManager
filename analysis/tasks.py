from celery import shared_task
from django.utils import translation

from analysis.notifications import WeekReportNotificationBuilder, DayTaskNotificationBuilder, DayTaskNotificationFetcher
from common.notifications import UserNotificationManger
from users.models import User
from .management.commands.make_summary import Command


@shared_task
def make_summary(username, start_date, end_date, tasks_ids, period):
    Command().handle(username=username, start_date=start_date, end_date=end_date, tasks_ids=tasks_ids, period=period)


@shared_task
def make_week_report():
    make_report(WeekReportNotificationBuilder)


@shared_task
def make_day_report():
    make_report(DayTaskNotificationBuilder, DayTaskNotificationFetcher)


def make_report(builder, fetcher=None):
    users = User.objects.all()
    for user in users:
        with translation.override(user.language):
            user_notification_manager = UserNotificationManger(user=user, builder=builder, fetcher=fetcher)
            user_notification_manager.notify()
