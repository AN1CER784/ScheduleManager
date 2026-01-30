import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.utils import delete_object
from tasks.mixins import TasksMixin

logger = logging.getLogger(__name__)


class DeleteTaskView(LoginRequiredMixin, TasksMixin, View):
    def post(self, request, *args, **kwargs):
        """??????? ?????? ?? id ? ????????? ???????? ? ?????????? ??????."""
        try:
            task = self.get_task(request)
            if task is None:
                return JsonResponse(self.response(message=_("Task not found"), item_html="", success=False), status=404)
            item_html = self.render_task(task=task, request=request, project=task.project)
            delete_object(model_object=task)
            return JsonResponse(self.response(message=_('Task was deleted'), item_html=item_html, success=True))
        except Exception as exc:
            logger.exception("Failed to delete task", exc_info=exc)
            return JsonResponse(self.response(message=_("Task was not deleted"), item_html="", success=False), status=500)
