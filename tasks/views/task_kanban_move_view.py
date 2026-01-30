import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import View

from tasks.mixins import TasksMixin
from tasks.models import Task
from tasks.services.bonus import apply_bonus, get_bonus_points_on_time
from tasks.services.workflow import can_transition
from tasks.utils import log_task_changes


class TaskKanbanMoveView(LoginRequiredMixin, TasksMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.body.decode("utf-8"))
        except json.JSONDecodeError:
            return JsonResponse(self.response(message=_("Invalid payload"), item_html="", success=False), status=400)

        task_id = payload.get("task_id")
        new_status = payload.get("new_status")
        target_order = [int(x) for x in (payload.get("target_order") or []) if x]
        source_order = [int(x) for x in (payload.get("source_order") or []) if x]

        task = (Task.objects
                .select_related("project", "assignee", "creator")
                .filter(id=task_id, project__company=request.user.company)
                .first())
        if task is None or new_status not in Task.Status.values:
            return JsonResponse(self.response(message=_("Invalid task or status"), item_html="", success=False), status=404)

        old_status = task.status
        old_position = task.position

        if new_status != old_status and not can_transition(task, request.user, new_status):
            return JsonResponse(self.response(message=_("Status change not allowed"), item_html="", success=False), status=403)

        if task.id not in target_order:
            target_order.append(task.id)

        with transaction.atomic():
            if new_status != old_status:
                task.status = new_status
                if new_status == Task.Status.DONE:
                    task.completed_at = timezone.now()
                task.save(update_fields=["status", "completed_at"])

            if target_order:
                self._apply_order(task.project_id, new_status, target_order)
            if source_order and old_status != new_status:
                self._apply_order(task.project_id, old_status, source_order)

            if new_status != old_status:
                log_task_changes(task, request.user, {"status": (old_status, new_status)})

            if new_status == Task.Status.DONE and task.deadline and task.completed_at <= task.deadline:
                apply_bonus(task.assignee, task, get_bonus_points_on_time(), _("On-time completion"))

        task.refresh_from_db()
        return JsonResponse({
            "success": True,
            "task_id": task.id,
            "status": task.status,
            "position": task.position,
        })

    @staticmethod
    def _apply_order(project_id, status, ordered_ids):
        for index, task_id in enumerate(ordered_ids, start=1):
            Task.objects.filter(id=task_id, project_id=project_id, status=status).update(position=index)
