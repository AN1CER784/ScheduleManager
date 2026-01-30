import logging

from django.http import JsonResponse
from django.views import View
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from common.mixins import JsonFormMixin
from tasks.forms import TaskCommentForm
from tasks.mixins import TasksMixin

logger = logging.getLogger(__name__)


class TaskEditCommentView(LoginRequiredMixin, JsonFormMixin, TasksMixin, View):
    form_class = TaskCommentForm
    comment = None

    def post(self, request, *args, **kwargs):
        """????????? ??????????? ? ????????? ????????????? ? ????????."""
        try:
            self.comment = self.get_comment(request)
            if self.comment is None:
                return JsonResponse(self.response(message=_("Comment not found"), item_html="", success=False), status=404)
            return super().post(request, *args, **kwargs)
        except Exception as exc:
            logger.exception("Failed to edit comment", exc_info=exc)
            return JsonResponse(self.response(message=_("Comment was not edited"), item_html="", success=False), status=500)

    def get_form_kwargs(self):
        """?????????????? kwargs ??? ????? ?????????????? ???????????."""
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.comment
        return kwargs

    def form_valid(self, form):
        """????????? ????????? ??????????? ? ?????????? HTML."""
        comment = form.save()
        item_html = self.render_comment(comment=comment, request=self.request, project=comment.task.project)
        return JsonResponse(self.response(message=_('Comment was successfully edited'), item_html=item_html, success=True))

    def form_invalid(self, form):
        """?????????? ?????? ????????? ??? ????? ?????????????? ???????????."""
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message=_('Comment was not edited'), item_html=item_html, success=False))
