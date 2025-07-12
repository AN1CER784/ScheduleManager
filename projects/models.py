from typing import Self

from django.db import models
from django.db.models import Count, Q, F, Case, When, Value, ExpressionWrapper, Min, Max, CharField, \
    IntegerField
from django.db.models.functions import Cast, Concat
from django.utils.translation import gettext as _
from common.models import AbstractCreatedModel


class ProjectQuerySet(models.QuerySet):
    def get_projects_periods(self) -> Self:
        projects = self.annotate(
            earliest=Min('tasks__start_datetime__date'),
            latest=Max('tasks__due_datetime__date')
        ).annotate(
            term=Case(
                When(earliest__isnull=True, then=Value(_("No term"))),
                When(
                    latest__isnull=True,
                    then=Concat(
                        Value(_("Start "), output_field=CharField()),
                        Cast('earliest', CharField())
                    )
                ),
                default=Concat(
                    Value(_("Start "),  output_field=CharField()),
                    Cast('earliest', CharField()), 
                    Value(_(" To "),  output_field=CharField()),
                    Cast('latest', CharField())
                ),
                output_field=CharField()
            )
        )
        return projects

    def get_projects_percent_complete(self) -> Self:
        projects = self.annotate(
            total=Count('tasks'),
            completed=Count('tasks', filter=Q(tasks__is_completed=True)),
        ).annotate(
            percent_complete=Case(
                When(total=0, then=Value(0)),
                default=ExpressionWrapper(F('completed') * 100.0 / F('total'), output_field=IntegerField()),
                output_field=IntegerField(),
            )
        )
        return projects


class Project(AbstractCreatedModel):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)

    class Meta:
        verbose_name = 'project'
        ordering = ['created_at']

    objects = ProjectQuerySet.as_manager()

