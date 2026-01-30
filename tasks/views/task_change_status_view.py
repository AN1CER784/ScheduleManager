from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models, transaction
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from tasks.mixins import TasksMixin
from tasks.models import Task
from tasks.services.bonus import apply_bonus, get_bonus_points_on_time
from tasks.services.workflow import transition_task_status, TaskStatusError
from tasks.utils import log_task_changes


class TaskChangeStatusView(LoginRequiredMixin, TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        new_status = request.POST.get("new_status")
        if task is None or new_status not in Task.Status.values:
            return JsonResponse(self.response(message=_('Invalid task or status'), item_html="", success=False))
        old_status = task.status
        old_position = task.position
        try:
            with transaction.atomic():
                transition_task_status(task=task, user=request.user, new_status=new_status)
                if task.status != old_status:
                    task.position = (Task.objects
                                     .filter(project=task.project, status=task.status)
                                     .exclude(id=task.id)
                                     .aggregate(max_pos=models.Max("position"))
                                     .get("max_pos") or 0) + 1
                    task.save(update_fields=["position"])
                log_task_changes(task, request.user, {"status": (old_status, task.status)})
                if task.status == Task.Status.DONE and task.deadline and task.completed_at <= task.deadline:
                    apply_bonus(task.assignee, task, get_bonus_points_on_time(), _("On-time completion"))
        except TaskStatusError:
            return JsonResponse(self.response(message=_('Status change not allowed'), item_html="", success=False))
        card_html = self.render_task_card(task=task, request=request, project=task.project)
        detail_html = self.render_task_detail(task=task, request=request, project=task.project)
        return JsonResponse(self.response(message=_('Task status was updated'), item_html=card_html, success=True,
                                          status=task.status, detail_html=detail_html, old_status=old_status,
                                          old_position=old_position))
