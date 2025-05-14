from django.db import models


class TaskQuerySet(models.QuerySet):
    def get_pending(self):
        return self.filter(status=None)

    def get_done(self):
        return self.exclude(status=None)



class Task(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    description = models.TextField(null=True, blank=True)
    status = models.BooleanField(default=None,
                                 choices=[(None, 'Pending'), (False, 'Could not complete'), (True, 'Completed')], null=True, blank=True)
    status_comment = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'task'
        ordering = ['date', 'time']

    objects = TaskQuerySet.as_manager()