from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from projects.mixins import ProjectMixin
from tasks.mixins import TasksMixin
from tasks.models import Task
from tasks.services.filters import apply_task_filters


class TaskKanbanListView(LoginRequiredMixin, ProjectMixin, TasksMixin, View):
    slug_url_kwarg = "id"

    def get(self, request, *args, **kwargs):
        project = self.get_project(project_id=self.kwargs.get(self.slug_url_kwarg), user=request.user)
        status = request.GET.get("column_status") or request.GET.get("status")
        if status not in Task.Status.values:
            return JsonResponse(self.response(message=_("Invalid status"), item_html="", success=False), status=400)

        statuses = request.GET.getlist("status")
        if statuses and status not in statuses:
            return JsonResponse({
                "success": True,
                "items_html": "",
                "has_next": False,
                "next_page": 1,
                "total": 0,
            })

        queryset = (Task.objects
                    .select_related("assignee", "creator", "project")
                    .filter(project=project, status=status))
        queryset = apply_task_filters(queryset, request.GET)
        queryset = queryset.order_by("position", "deadline", "created_at", "id")

        page = max(int(request.GET.get("page", 1)), 1)
        page_size = min(max(int(request.GET.get("page_size", 20)), 1), 50)
        start = (page - 1) * page_size
        end = start + page_size + 1
        items = list(queryset[start:end])
        has_next = len(items) > page_size
        items = items[:page_size]

        items_html = "".join(self.render_task_card(task=task, request=request, project=project) for task in items)
        total = queryset.count()
        return JsonResponse({
            "success": True,
            "items_html": items_html,
            "has_next": has_next,
            "next_page": page + 1,
            "total": total,
        })
