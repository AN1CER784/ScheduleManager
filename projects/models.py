from django.db import models
from django.db.models import Count, Q, F, Case, When, Value, FloatField, ExpressionWrapper, Min, Max, CharField
from django.db.models.functions import Cast, Concat


class ProjectQuerySet(models.QuerySet):
    def get_projects_periods(self):
        projects = self.annotate(
            earliest=Min('tasks__start_datetime'),
            latest=Max('tasks__due_datetime')
        ).annotate(
            term=Case(
                When(earliest__isnull=True, then=Value("No term")),
                When(
                    latest__isnull=True,
                    then=Concat(
                        Value("Start "),
                        Cast('earliest', CharField())
                    )
                ),
                default=Concat(
                    Value("Start "),
                    Cast('earliest', CharField()),
                    Value(" To "),
                    Cast('latest', CharField())
                ),
                output_field=CharField()
            )
        )
        return projects

    def get_projects_percent_complete(self):
        projects = self.annotate(
            total=Count('tasks'),
            completed=Count('tasks', filter=Q(tasks__is_completed=True)),
        ).annotate(
            percent_complete=Case(
                When(total=0, then=Value(0)),
                default=ExpressionWrapper(F('completed') * 100.0 / F('total'), output_field=FloatField()),
                output_field=FloatField(),
            )
        )
        return projects


class Project(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='projects', blank=True, null=True)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    name = models.CharField(max_length=100, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'project'
        ordering = ['created_at']

    objects = ProjectQuerySet.as_manager()
