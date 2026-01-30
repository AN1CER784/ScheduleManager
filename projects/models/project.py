from django.conf import settings
from django.db import models

from common.models import AbstractCreatedModel


class ProjectQuerySet(models.QuerySet):
    pass


class Project(AbstractCreatedModel):
    company = models.ForeignKey('users.Company', on_delete=models.CASCADE, related_name='projects')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True,
                                   related_name='created_projects')
    participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='project_participants', blank=True)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'project'
        ordering = ['created_at']

    objects = ProjectQuerySet.as_manager()
