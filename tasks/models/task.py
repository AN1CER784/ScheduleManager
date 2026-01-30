from typing import NamedTuple

from django.conf import settings
from django.db import models
from django.utils import timezone

from common.models import AbstractCreatedModel


class TaskByStatus(NamedTuple):
    new: list["Task"]
    in_progress: list["Task"]
    on_review: list["Task"]
    done: list["Task"]


class TaskQuerySet(models.QuerySet):
    def split_by_status(self) -> TaskByStatus:
        tasks = (self.all()
                 .select_related("assignee", "creator", "project")
                 .prefetch_related("comments", "results", "change_logs")
                 .order_by("position", "deadline", "created_at"))
        new = [t for t in tasks if t.status == Task.Status.NEW]
        in_progress = [t for t in tasks if t.status == Task.Status.IN_PROGRESS]
        on_review = [t for t in tasks if t.status == Task.Status.ON_REVIEW]
        done = [t for t in tasks if t.status == Task.Status.DONE]
        return TaskByStatus(new=new, in_progress=in_progress, on_review=on_review, done=done)


class Task(AbstractCreatedModel):
    class Status(models.TextChoices):
        NEW = "NEW", "New"
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        ON_REVIEW = "ON_REVIEW", "On review"
        DONE = "DONE", "Done"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='created_tasks')
    assignee = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='assigned_tasks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    position = models.PositiveIntegerField(default=0, db_index=True)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
    deadline = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    overdue_penalty_applied = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'task'
        ordering = ['position', 'deadline', 'created_at']

    objects = TaskQuerySet.as_manager()

    @property
    def is_done(self) -> bool:
        return self.status == Task.Status.DONE

    @property
    def is_overdue(self) -> bool:
        return bool(self.deadline and self.deadline < timezone.now() and not self.is_done)

    def mark_completed(self) -> None:
        self.completed_at = timezone.now()
