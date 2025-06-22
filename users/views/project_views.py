from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from projects.mixins import ProjectMixin
from projects.models import Project


class UserTasksView(ProjectMixin, DetailView):
    template_name = 'tasks/tasks.html'
    success_url = reverse_lazy('users:tasks')
    context_object_name = 'project'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Schedule'
        return context

    def get_object(self, queryset=None):
        project = self.get_project(user_id=self.request.user.id, project_id=self.kwargs.get(self.slug_url_kwarg),
                                   session_key=self.request.session.session_key)
        return project


class UserProjectsView(ListView):
    template_name = 'projects/projects.html'
    success_url = reverse_lazy('users:projects')
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Projects'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            projects = Project.objects.filter(user=self.request.user)
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            projects = Project.objects.filter(session_key=self.request.session.session_key)
        projects = projects.prefetch_related('tasks').get_projects_percent_complete().get_projects_periods()
        return projects
