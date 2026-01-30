from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.mixins import JsonFormMixin
from projects.mixins import ProjectMixin
from tasks.forms import TaskCreateForm
from tasks.mixins import TasksMixin


class AddTaskView(LoginRequiredMixin, JsonFormMixin, ProjectMixin, TasksMixin, View):
    form_class = TaskCreateForm
    slug_url_kwarg = 'id'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        project = self.get_project(project_id=self.kwargs.get(self.slug_url_kwarg), user=self.request.user)
        task = form.save(commit=False)
        task.project = project
        task.creator = self.request.user
        task.position = (project.tasks
                         .filter(status=task.status)
                         .aggregate(max_pos=models.Max("position"))
                         .get("max_pos") or 0) + 1
        task.save()
        project.participants.add(self.request.user, task.assignee)
        card_html = self.render_task_card(task=task, request=self.request, project=project)
        detail_html = self.render_task_detail(task=task, request=self.request, project=project)
        return JsonResponse(self.response(message=_('Task was successfully added'), item_html=card_html,
                                          success=True, status=task.status, detail_html=detail_html))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(_('Task was not added'), item_html, False))
