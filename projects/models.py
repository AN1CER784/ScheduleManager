from django.db import models

class Project(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'project'
        ordering = ['created_at']

