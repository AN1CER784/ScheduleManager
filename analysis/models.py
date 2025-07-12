from django.db import models

from common.models import AbstractCreatedModel
from users.models import User
from django.core.cache import cache

PERIOD_CHOICES = [
    (1, 'Daily'),
    (7, 'Weekly'),
]


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


class AnalysisSummary(models.Model):
    report = models.OneToOneField(AnalysisReport, on_delete=models.CASCADE, related_name='summary', blank=False,
                                  null=False)
    summary = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'summary'
        ordering = ['report__start_date', 'report__end_date']


class AnalysisPrompt(models.Model):
    period = models.IntegerField(choices=PERIOD_CHOICES, blank=False, null=False, primary_key=True)
    prompt = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'prompt'
