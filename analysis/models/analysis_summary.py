from django.db import models

from analysis.models.analysis_report import AnalysisReport


class AnalysisSummary(models.Model):
    report = models.OneToOneField(AnalysisReport, on_delete=models.CASCADE, related_name='summary', blank=False,
                                  null=False)
    summary = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'summary'
        ordering = ['report__start_date', 'report__end_date']
