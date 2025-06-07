from django.db import models


class TaskQuerySet(models.QuerySet):
    def get_pending(self):
        return self.filter(is_completed=False)

    def get_done(self):
        return self.filter(is_completed=True)

class Task(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tasks',  blank=True, null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    start_datetime = models.DateTimeField(blank=True, null=True)
    due_datetime = models.DateTimeField(blank=True, null=True)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    session_key = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        verbose_name = 'task'
        ordering = ['created_at']

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
