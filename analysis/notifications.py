from django.template.loader import render_to_string
from django.utils import timezone

from analysis.utils import get_or_create_report
from tasks.models import Task


class BaseNotificationBuilder:
    template_html = 'analysis/emails/report_email.html'
    template_text = 'analysis/emails/report_email_text.html'
    period = None
    subject = None

    @classmethod
    def build(cls, user, tasks=None):
        recipient_list = [user.email]
        days = 7 if cls.period == 'Week' else 1
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
    subject = 'Week analysis report'
    period = 'Week'


class DayTaskNotificationBuilder(BaseNotificationBuilder):
    subject = 'Day analysis report'
    period = 'Day'



class DayTaskNotificationFetcher:
    @staticmethod
    def fetch(user):
        return (
            Task.objects
            .filter(project__user=user, is_completed=False, due_datetime__lt=timezone.now())
            .select_related('project')
        )