from django.http import JsonResponse

from django.views import View

from projects.mixins import ProjectMixin
from tasks.forms import TaskCreateForm, TaskCompleteForm, TaskIncompleteForm, TaskUpdateForm
from tasks.mixins import TasksMixin
from common.mixins import JsonFormMixin





class AddTaskView(JsonFormMixin, ProjectMixin, TasksMixin, View):
    form_class = TaskCreateForm
    slug_url_kwarg = 'id'

    def form_valid(self, form):
        task = form.save(commit=False)
        task.project = self.get_project(user_id=self.request.user.id, project_id=self.kwargs.get(self.slug_url_kwarg), session_key=self.request.session.session_key)
        task.save()
        item_html = self.render_task(task=task, request=self.request, project=task.project)
        return JsonResponse(self.response(message='Task was successfully added', item_html=item_html, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response('Task was not added', item_html, False))


class DeleteTaskView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        item_html = self.render_task(task=task, request=request, project=task.project)
        task.delete()
        return JsonResponse(self.response(message='Task was deleted', item_html=item_html, success=True))


class CompleteTaskView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        form = TaskCompleteForm(request.POST, instance=task)
        form.save()
        item_html = self.render_task(task=task, task_type='Done', request=request, project=task.project)
        return JsonResponse(self.response(message='Task was successfully completed', item_html=item_html, success=True))


class IncompleteTaskView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        form = TaskIncompleteForm(request.POST, instance=task)
        form.save()
        item_html = self.render_task(task=task, request=request, project=task.project)
        return JsonResponse(self.response(message='Task was successfully incompleted', item_html=item_html, success=True))


class TaskUpdateProgressView(TasksMixin, View):
    def post(self, request, *args, **kwargs):
        task = self.get_task(request)
        task.progress.percentage = int(request.POST.get('complete_percentage'))
        task.progress.save()
        item_html = self.render_task(task=task, request=request, project=task.project)
        return JsonResponse(self.response(message='Task progress was successfully updated', item_html=item_html, success=True))

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
        return JsonResponse(self.response(message='Task was successfully updated', item_html=item_html, success=True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(message='Task was not updated', item_html=item_html, success=False))