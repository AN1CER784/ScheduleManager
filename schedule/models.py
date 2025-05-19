from django.db import models


class TaskQuerySet(models.QuerySet):
    def get_pending(self):
        return self.filter(is_completed=False)

    def get_done(self):
        return self.filter(is_completed=True)


class Task(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    start_time = models.TimeField()
    due_date = models.DateField()
    due_time = models.TimeField()
    description = models.TextField()
    complete_datetime = models.DateTimeField(blank=True, null=True)
    complete_percentage = models.IntegerField(default=5)
    is_completed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'task'
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.complete_percentage == 100:
            self.is_completed = True
        else:
            self.is_completed = False
        super().save()

    objects = TaskQuerySet.as_manager()


class TaskComment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_date = models.DateField(auto_now=True)
    created_time = models.TimeField(auto_now=True)

    class Meta:
        verbose_name = 'task_comment'
        ordering = ['created_date', 'created_time']
