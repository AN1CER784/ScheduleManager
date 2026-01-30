from django.conf import settings
from django.db import models

from common.models import AbstractCreatedModel


class BonusTransaction(AbstractCreatedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bonus_transactions")
    task = models.ForeignKey('tasks.Task', on_delete=models.SET_NULL, null=True, blank=True,
                             related_name="bonus_transactions")
    points = models.IntegerField()
    reason = models.CharField(max_length=200)

    class Meta:
        verbose_name = "bonus_transaction"
        ordering = ["-created_at"]
