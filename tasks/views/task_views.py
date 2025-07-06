from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.common_services import delete_object
from common.mixins import JsonFormMixin
from projects.mixins import ProjectMixin
from tasks.forms import TaskCreateForm, TaskUpdateForm
from tasks.mixins import TasksMixin
from tasks.task_update_service import create_task_with_progress, update_progress


class AddTaskView(JsonFormMixin, ProjectMixin, TasksMixin, View):
    form_class = TaskCreateForm
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.project = self.get_project(user_id=self.request.user.id, project_id=self.kwargs.get(self.slug_url_kwarg),
                                        session_key=self.request.session.session_key)
        create_task_with_progress(task=task)
        item_html = self.render_task(task=task, request=self.request, project=task.project)
        return JsonResponse(self.response(message=_('Task was successfully added'), item_html=item_html, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(_('Task was not added'), item_html, False))


class DeleteTaskView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        item_html = self.render_task(task=task, request=request, project=task.project)
        delete_object(model_object=task)
        return JsonResponse(self.response(message=_('Task was deleted'), item_html=item_html, success=True))


class CompleteTaskView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        update_progress(progress=task.progress, percentage=100)
        item_html = self.render_task(task=task, task_type='Done', request=request, project=task.project)
        return JsonResponse(
            self.response(message=_('Task was successfully completed'), item_html=item_html, success=True))


class IncompleteTaskView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        update_progress(progress=task.progress, percentage=5)
        item_html = self.render_task(task=task, request=request, project=task.project)
        return JsonResponse(
            self.response(message=_('Task was successfully incompleted'), item_html=item_html, success=True))


class TaskUpdateProgressView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        update_progress(progress=task.progress, percentage=int(request.POST.get('complete_percentage')))
        item_html = self.render_task(task=task, request=request, project=task.project)
        return JsonResponse(
            self.response(message=_('Task progress was successfully updated'), item_html=item_html, success=True))


class TaskUpdateInfoView(TasksMixin, JsonFormMixin, View):
    form_class = TaskUpdateForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_task(self.request)
        kwargs['instance'] = instance
        return kwargs

    def form_valid(self, form):
        task = form.save()
        task_type = 'Done' if task.is_completed else "InProgress"
        item_html = self.render_task(task=task, request=self.request, project=task.project, task_type=task_type)
        return JsonResponse(
            self.response(message=_('Task was successfully updated'), item_html=item_html, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message=_('Task was not updated'), item_html=item_html, success=False))
