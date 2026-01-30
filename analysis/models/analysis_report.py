from django.core.cache import cache
from django.db import models

from analysis.models.constants import PERIOD_CHOICES
from users.models import User


class AnalysisReportQuerySet(models.QuerySet):
    def get_reports(self, user: User) -> dict[int, list['AnalysisReport']]:
        cache_key = f'summaries_for_user_{user.id}'
        data = cache.get(cache_key)
        if data is not None:
            return data
        reports = self.filter(user=user)
        dict_periods = {}
        for period in (1, 7):
            reports_by_period = [report for report in reports if report.period == period and bool(
                getattr(getattr(report, 'summary', None), 'summary', None))]
            dict_periods[period] = reports_by_period
        cache.set(cache_key, dict_periods, 60)
        return dict_periods


class AnalysisReport(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, blank=False, null=False)
    period = models.IntegerField(choices=PERIOD_CHOICES, blank=False, null=False)
    report = models.JSONField(blank=False, null=False)
    start_date = models.DateField(blank=False, null=False)
    end_date = models.DateField(blank=False, null=False)

    objects = AnalysisReportQuerySet.as_manager()

    class Meta:
        verbose_name = 'report'
        ordering = ['start_date', "end_date"]
