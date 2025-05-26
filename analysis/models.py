from django.db import models


class AnalysisSummaryQuerySet(models.QuerySet):
    def get_summaries_by_period(self, period, user):
        return self.filter(period=period, user=user)


class AnalysisSummary(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    summary = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    period = models.IntegerField()

    objects = AnalysisSummaryQuerySet.as_manager()