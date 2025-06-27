from django.db import models

from common.models import AbstractCreatedModel

PERIOD_CHOICES = [
    (1, 'Daily'),
    (7, 'Weekly'),
]

class AnalysisReportQuerySet(models.QuerySet):
    def get_reports_by_period(self, periods, user):
        reports = self.filter(user=user)
        dict_periods = {}
        for period in periods:
            reports_by_period = [report for report in reports if report.period == period and hasattr(report, 'summary')]
            dict_periods[period] = reports_by_period
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
    report = models.OneToOneField(AnalysisReport, on_delete=models.CASCADE, related_name='summary', blank=False, null=False)
    summary = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'summary'
        ordering = ['report__start_date', 'report__end_date']


class AnalysisPrompt(models.Model):
    period = models.IntegerField(choices=PERIOD_CHOICES, blank=False, null=False, primary_key=True)
    prompt = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'prompt'