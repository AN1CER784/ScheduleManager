from django.conf import settings
from django.db import models

from common.models import AbstractCreatedModel
from tasks.models.task import Task


class TaskResult(AbstractCreatedModel):
    class ResultType(models.TextChoices):
        MESSAGE = "MESSAGE", "Message"

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='results')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='task_results')
    result_type = models.CharField(max_length=20, choices=ResultType.choices, default=ResultType.MESSAGE)
    message = models.TextField()

    class Meta:
        verbose_name = "task_result"
        ordering = ["created_at"]
