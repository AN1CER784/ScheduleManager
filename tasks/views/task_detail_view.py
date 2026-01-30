from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from tasks.mixins import TasksMixin


class TaskDetailView(LoginRequiredMixin, TasksMixin, View):
    def get(self, request, *args, **kwargs):
        task_id = request.GET.get("task_id")
        task = (self.get_task_from_id(task_id=task_id, request=request))
        if task is None:
            return JsonResponse({"success": False, "message": _("Task not found")}, status=404)
        detail_html = self.render_task_detail(task=task, request=request, project=task.project)
        return JsonResponse({"success": True, "detail_html": detail_html})
