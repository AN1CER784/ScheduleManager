from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.utils.translation import gettext_lazy as _

from common.utils import delete_object
from common.mixins import JsonFormMixin
from tasks.forms import TaskCommentForm
from tasks.mixins import TasksMixin


class TaskAddCommentView(JsonFormMixin, TasksMixin, View):
    form_class = TaskCommentForm

    def form_valid(self, form):
        task = self.get_task(self.request)
        comment = form.save(commit=False)
        comment.task = task
        comment.save()
        item_html = self.render_comment(comment=comment, request=self.request, project=task.project)
        divider_html = render_to_string(template_name='tasks/includes/comment_divider.html', context={
            'comment_date': comment.created_date
        }, request=self.request)
        return JsonResponse(
            self.response(message=_('Comment was successfully added'), item_html=item_html, success=True,
                          divider_html=divider_html,
                          comment_date=comment.created_date))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message=_('Comment was not added'), item_html=item_html, success=False))


class TaskDeleteCommentView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        comment = self.get_comment(request)
        item_html = self.render_comment(comment=comment, request=request, project=comment.task.project)
        delete_object(model_object=comment)
        return JsonResponse(self.response(message=_('Comment was deleted'), item_html=item_html, success=True))


class TaskEditCommentView(JsonFormMixin, TasksMixin, View):
    form_class = TaskCommentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_comment(self.request)
        return kwargs

    def form_valid(self, form):
        comment = form.save()
        item_html = self.render_comment(comment=comment, request=self.request, project=comment.task.project)
        return JsonResponse(self.response(message=_('Comment was successfully edited'), item_html=item_html, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message=_('Comment was not edited'), item_html=item_html, success=False))
