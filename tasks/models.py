from django.db import models

from common.models import AbstractCreatedModel


class TaskQuerySet(models.QuerySet):
    def split_pending_done(self):
        tasks = self.all().select_related("progress").prefetch_related("comments")
        pending = [t for t in tasks if not t.is_completed]
        done = [t for t in tasks if t.is_completed]
        return {
            "pending": pending,
            "done": done
        }


class Task(AbstractCreatedModel):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks', blank=False, null=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    start_datetime = models.DateTimeField(blank=False, null=False)
    due_datetime = models.DateTimeField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        task_id = self.id
        super().save(*args, **kwargs)
        if task_id is None:
            TaskProgress.objects.create(task=self)

    class Meta:
        verbose_name = 'task'
        ordering = ['due_datetime']

    objects = TaskQuerySet.as_manager()


class TaskComment(AbstractCreatedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments', blank=False, null=False)
    text = models.TextField(blank=False, null=False)

    @property
    def created_date(self):
        return self.created_at.date()

    @property
    def created_time(self):
        return self.created_at.time()

    class Meta:
        verbose_name = 'task_comment'
        ordering = ['created_at']



class TaskProgress(models.Model):
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='progress', blank=False, null=False)
    percentage = models.PositiveIntegerField(default=5)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'task_progress'
        ordering = ['updated_datetime']

    def save(self, *args, **kwargs):
        if self.percentage == 100:
            Task.objects.filter(id=self.task_id).update(is_completed=True)
        else:
            Task.objects.filter(id=self.task_id).update(is_completed=False)
        super().save(*args, **kwargs)
