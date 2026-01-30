import logging

from django.http import JsonResponse
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from common.utils import delete_object
from tasks.mixins import TasksMixin

logger = logging.getLogger(__name__)


class TaskDeleteCommentView(LoginRequiredMixin, TasksMixin, View):
    def post(self, request, *args, **kwargs):
        """??????? ??????????? ?? id ? ????????? ???????? ? ?????????? ??????."""
        try:
            comment = self.get_comment(request)
            if comment is None:
                return JsonResponse(self.response(message=_("Comment not found"), item_html="", success=False), status=404)
            item_html = self.render_comment(comment=comment, request=request, project=comment.task.project)
            delete_object(model_object=comment)
            return JsonResponse(self.response(message=_('Comment was deleted'), item_html=item_html, success=True))
        except Exception as exc:
            logger.exception("Failed to delete comment", exc_info=exc)
            return JsonResponse(self.response(message=_("Comment was not deleted"), item_html="", success=False), status=500)
