from django.conf import settings
from django.db import models

from common.models import AbstractCreatedModel
from tasks.models.task import Task


class TaskChangeLog(AbstractCreatedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='change_logs')
    changed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_change_logs')
    field_name = models.CharField(max_length=50)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "task_change_log"
        ordering = ["-created_at"]
