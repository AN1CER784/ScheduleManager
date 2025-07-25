from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, DetailView

from common.mixins import SessionMixin
from projects.mixins import ProjectMixin
from projects.models import Project


class UserTasksView(ProjectMixin, DetailView):
    template_name = 'tasks/tasks.html'
    success_url = reverse_lazy('users:tasks')
    context_object_name = 'project'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Schedule')
        return context

    def get_object(self, queryset=None):
        project = self.get_project(user_id=self.request.user.id, project_id=self.kwargs.get(self.slug_url_kwarg),
                                   session_key=self.request.session.session_key)
        return project


class UserProjectsView(SessionMixin, ListView):
    template_name = 'projects/projects.html'
    success_url = reverse_lazy('users:projects')
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Projects')
        return context

    def get_queryset(self):
        projects = self.get_owner_filter(model=Project)
        projects = projects.prefetch_related('tasks').get_projects_percent_complete().get_projects_periods()
        return projects
