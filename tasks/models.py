from django.db import models


class TaskQuerySet(models.QuerySet):
    def get_pending(self):
        return self.filter(is_completed=False)

    def get_done(self):
        return self.filter(is_completed=True)

    def get_proj_period(self):
        if self.count() == 0:
            return "No term"

        earliest_task = self.order_by('start_datetime')[0]
        latest_task = self.order_by('-due_datetime') \
            .filter(due_datetime__isnull=False)[0]

        if not latest_task.due_datetime:
            return f"Term: since {earliest_task.start_datetime.date()}"
        return f"Term: since {earliest_task.start_datetime.date()} to {latest_task.due_datetime.date()}"

    def get_percent_completion(self):
        total_tasks = self.count()
        completed_tasks = self.filter(is_completed=True).count()
        return (completed_tasks / total_tasks) * 100 if total_tasks > 0 else 0


class Task(models.Model):
    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    due_datetime = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
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
    text = models.TextField()
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
    percentage = models.IntegerField(default=5)
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


