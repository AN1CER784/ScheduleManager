from django.db import models

from analysis.models.constants import PERIOD_CHOICES


class AnalysisPrompt(models.Model):
    period = models.IntegerField(choices=PERIOD_CHOICES, blank=False, null=False, primary_key=True)
    prompt = models.TextField(blank=False, null=False)

    class Meta:
        verbose_name = 'prompt'
