from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView

from projects.models import Project


class UserProjectsView(LoginRequiredMixin, ListView):
    template_name = 'projects/projects.html'
    success_url = reverse_lazy('users:projects')
    context_object_name = 'projects'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Projects')
        return context

    def get_queryset(self):
        return (Project.objects.filter(company=self.request.user.company)
                .annotate(tasks_count=Count('tasks'), members_count=Count('participants', distinct=True)))
