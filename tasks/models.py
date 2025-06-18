from django.db import models



class TaskQuerySet(models.QuerySet):
    def split_pending_done(self):
        tasks = self.all().select_related("progress").prefetch_related("comments")
        pending = [t for t in tasks if not t.is_completed]
        done = [t for t in tasks if t.is_completed]
        return {
            "pending": pending,
            "done": done
        }


class Task(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
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


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

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
    task = models.OneToOneField(Task, on_delete=models.CASCADE, related_name='progress')
    percentage = models.PositiveIntegerField(default=5)
    updated_datetime = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'task_progress'
        ordering = ['updated_datetime']

    def save(self, *args, **kwargs):
        if self.percentage == 100:
            self.task.is_completed = True
        else:
            self.task.is_completed = False
        self.task.save()
        super().save(*args, **kwargs)
