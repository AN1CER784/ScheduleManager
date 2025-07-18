from datetime import datetime
from typing import Literal

from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from analysis.models import AnalysisSummary, AnalysisReport
from analysis.tasks import make_summary
from analysis.services.reports import get_or_create_report
from tasks.models import Task, TaskQuerySet
from users.models import User


class AnalysisGenerator:
    def __init__(self, user: User, period: Literal[1, 7], start_date: datetime.date, end_date: datetime.date):
        self.user = user
        self.period = period
        self.start_date = start_date
        self.end_date = end_date
        self.report = None
        self.tasks = None

    def _get_tasks_in_range(self) -> TaskQuerySet:
        return Task.objects.filter(
            project__user=self.user
        ).filter(
            Q(start_datetime__date__range=(self.start_date, self.end_date)) |
            Q(due_datetime__date__range=(self.start_date, self.end_date))
        ).select_related('project')

    def _get_or_create_report(self) -> AnalysisReport:
        return get_or_create_report(
            user=self.user,
            period=self.period,
            start_date=self.start_date,
            end_date=self.end_date
        )

    def _trigger_async_summary(self, report: AnalysisReport, tasks: TaskQuerySet) -> None:
        make_summary.delay(
            user_id=self.user.id,
            report_id=report.id,
            tasks_ids=list(tasks.values_list('id', flat=True)),
            period=self.period
        )

    def validate(self) -> None:
        self.report = self._get_or_create_report()
        if AnalysisSummary.objects.filter(report=self.report).exists():
            raise ValueError(_("A summary already exists for the selected period and date."))
        self.tasks = self._get_tasks_in_range()
        if not self.tasks.exists():
            raise ValueError(_("No tasks found for the selected period."))

    def generate(self) -> None:
        if self.report is None or self.tasks is None:
            self.validate()
        AnalysisSummary.objects.create(report=self.report)
        self._trigger_async_summary(self.report, self.tasks)
