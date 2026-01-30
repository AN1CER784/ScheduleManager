from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView

from projects.mixins import ProjectMixin
from tasks.models import Task
from tasks.services.filters import apply_task_filters


class UserTasksView(LoginRequiredMixin, ProjectMixin, DetailView):
    template_name = 'tasks/tasks.html'
    success_url = reverse_lazy('users:tasks')
    context_object_name = 'project'
    slug_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Tasks')
        context['assignees'] = self.request.user.company.users.all()
        context['creators'] = self.request.user.company.users.all()
        context['priorities'] = Task.Priority.choices
        context['statuses'] = Task.Status.choices
        context['status_labels'] = {value: label for value, label in Task.Status.choices}
        context['status_order'] = [
            Task.Status.NEW,
            Task.Status.IN_PROGRESS,
            Task.Status.ON_REVIEW,
            Task.Status.DONE,
        ]
        context['filters'] = {
            'assignee': self.request.GET.get('assignee', ''),
            'creator': self.request.GET.get('creator', ''),
            'priority': self.request.GET.get('priority', ''),
            'deadline': self.request.GET.get('deadline', ''),
            'q': self.request.GET.get('q', ''),
            'status': self.request.GET.getlist('status'),
        }

        def get_status_data(status):
            base_qs = (Task.objects
                       .select_related('assignee', 'creator', 'project')
                       .filter(project=self.object, status=status))
            filtered = apply_task_filters(base_qs, self.request.GET)
            return {
                'count': filtered.count(),
                'items': list(filtered.order_by('position', 'deadline', 'created_at', 'id')[:20]),
            }

        context['kanban'] = {
            Task.Status.NEW: get_status_data(Task.Status.NEW),
            Task.Status.IN_PROGRESS: get_status_data(Task.Status.IN_PROGRESS),
            Task.Status.ON_REVIEW: get_status_data(Task.Status.ON_REVIEW),
            Task.Status.DONE: get_status_data(Task.Status.DONE),
        }
        return context

    def get_object(self, queryset=None):
        project = self.get_project(project_id=self.kwargs.get(self.slug_url_kwarg), user=self.request.user)
        return project
