from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.mixins import JsonFormMixin
from tasks.forms import TaskUpdateForm
from tasks.mixins import TasksMixin
from tasks.utils import log_task_changes


class TaskUpdateInfoView(LoginRequiredMixin, TasksMixin, JsonFormMixin, View):
    form_class = TaskUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_task(self.request)
        kwargs['instance'] = instance
        kwargs["request"] = self.request
        return kwargs

    def form_valid(self, form):
        task = self.get_task(self.request)
        old_values = {
            "name": task.name,
            "description": task.description,
            "assignee": task.assignee,
            "priority": task.priority,
            "deadline": task.deadline,
        }
        task = form.save()
        new_values = {
            "name": task.name,
            "description": task.description,
            "assignee": task.assignee,
            "priority": task.priority,
            "deadline": task.deadline,
        }
        log_task_changes(task, self.request.user, {
            key: (old_values[key], new_values[key]) for key in old_values.keys()
        })
        task.project.participants.add(task.assignee)
        card_html = self.render_task_card(task=task, request=self.request, project=task.project)
        detail_html = self.render_task_detail(task=task, request=self.request, project=task.project)
        return JsonResponse(
            self.response(message=_('Task was successfully updated'), item_html=card_html, success=True,
                          status=task.status, detail_html=detail_html))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message=_('Task was not updated'), item_html=item_html, success=False))
