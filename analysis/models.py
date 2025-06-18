from django.db import models


class AnalysisSummaryQuerySet(models.QuerySet):
    def get_summaries_by_period(self, periods, user):
        summaries = self.filter(user=user)
        dict_periods = {}
        for period in periods:
            summaries_by_period = [summary for summary in summaries if summary.period == period]
            dict_periods[period]: summaries_by_period
        return dict_periods


class AnalysisSummary(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    summary = models.TextField(blank=False, null=False)
    created_at = models.DateField(auto_now_add=True)
    period = models.IntegerField(blank=False, null=False)
    objects = AnalysisSummaryQuerySet.as_manager()

