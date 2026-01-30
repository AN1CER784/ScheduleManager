from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.mixins import JsonFormMixin
from tasks.forms import TaskResultForm
from tasks.mixins import TasksMixin


class TaskAddResultView(LoginRequiredMixin, TasksMixin, JsonFormMixin, View):
    form_class = TaskResultForm

    def form_valid(self, form):
        task = self.get_task(self.request)
        result = form.save(commit=False)
        result.task = task
        result.author = self.request.user
        result.save()
        item_html = self.render_result(result=result, request=self.request, project=task.project)
        return JsonResponse(self.response(message=_('Result was added'), item_html=item_html, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message=_('Result was not added'), item_html=item_html, success=False))
