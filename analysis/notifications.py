from typing import Literal

from django.db.models import QuerySet
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from analysis.utils import get_or_create_report
from tasks.models import Task
from users.models import User


class BaseNotificationBuilder:
    template_html = 'analysis/emails/report_email.html'
    template_text = 'analysis/emails/report_email_text.html'
    period = None
    subject = None

    @classmethod
    def build(cls, user: User, tasks: QuerySet[Task] | None = None) -> tuple[str, str, list, str]:
        recipient_list = [user.email]
        days: Literal[1, 7] = 7 if cls.period == 'Week' else 1
        report = get_or_create_report(user=user, period=days)
        context = {
            'report': report,
            'subject': cls.subject,
            'period': cls.period,
        }
        if tasks:
            context['tasks'] = tasks

        html_message = render_to_string(cls.template_html, context)
        message = render_to_string(cls.template_text, context)

        return cls.subject, message, recipient_list, html_message


class WeekReportNotificationBuilder(BaseNotificationBuilder):
    subject = _('Week analysis report')
    period = _('Week')


class DayTaskNotificationBuilder(BaseNotificationBuilder):
    subject = _('Day analysis report')
    period = _('Day')


class DayTaskNotificationFetcher:
    @classmethod
    def fetch(cls, user: User):
        return (
            Task.objects
            .filter(project__user=user, is_completed=False, due_datetime__lt=timezone.now())
            .select_related('project')
        )
