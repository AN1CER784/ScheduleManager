from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from schedule.forms import TaskCreateForm, TaskCompleteForm, TaskIncompleteForm, TaskCommentForm
from schedule.mixins import ScheduleMixin, JsonFormMixin


class UserScheduleAddTask(JsonFormMixin, ScheduleMixin, View):
    form_class = TaskCreateForm

    def form_valid(self, form):
        task = form.save(commit=False)
        if self.request.user.is_authenticated:
            task.user = self.request.user
        else:
            if not self.request.session.session_key:
                self.request.session.create()
            task.session_key = self.request.session.session_key
        task.save()
        item_html = self.render_task(task=task, type='InProgress', request=self.request)
        return JsonResponse(self.response('Task was successfully added', item_html, True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response('Task was not added', item_html, False))


class UserScheduleDeleteTask(ScheduleMixin, View):
    def post(self, request):
        task = self.get_task(request)
        item_html = self.render_task(task=task, request=request)
        task.delete()
        return JsonResponse(self.response('Task was deleted', item_html, True))


class UserScheduleCompleteTask(ScheduleMixin, View):
    def post(self, request):
        task = self.get_task(request)
        form = TaskCompleteForm(request.POST, instance=task)
        form.save()
        item_html = self.render_task(task=task, type='Done', request=request)
        return JsonResponse(self.response('Task was successfully completed', item_html, True))


class UserScheduleIncompleteTask(ScheduleMixin, View):
    def post(self, request):
        task = self.get_task(request)
        form = TaskIncompleteForm(request.POST, instance=task)
        form.save()
        item_html = self.render_task(task=task, type='InProgress', request=request)
        return JsonResponse(self.response('Task was successfully incompleted', item_html, True))


class UserUpdateProgressTask(ScheduleMixin, View):
    def post(self, request):
        task = self.get_task(request)
        task.complete_percentage = int(request.POST.get('complete_percentage'))
        task.save()
        item_html = self.render_task(task=task, type='InProgress', request=request)
        return JsonResponse(self.response('Task progress was successfully updated', item_html, True))


class UserScheduleAddComment(JsonFormMixin, ScheduleMixin, View):
    form_class = TaskCommentForm

    def form_valid(self, form):
        task = self.get_task(self.request)
        comment = form.save(commit=False)
        comment.task = task
        comment.save()
        item_html = self.render_comment(comment=comment, request=self.request)
        divider_html = render_to_string('schedule/includes/comment_divider.html', {
            'comment_date': comment.created_date
        }, request=self.request)
        return JsonResponse(
            self.response('Comment was successfully added', item_html, True, divider_html=divider_html))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response('Comment was not added', item_html, False))


class UserScheduleDeleteComment(ScheduleMixin, View):
    def post(self, request):
        comment = self.get_comment(request)
        item_html = self.render_comment(comment=comment, request=request)
        comment.delete()
        return JsonResponse(self.response('Comment was deleted', item_html, True))


class UserScheduleEditComment(JsonFormMixin, ScheduleMixin, View):
    form_class = TaskCommentForm

    def form_valid(self, form):
        comment = self.get_comment(self.request)
        form.save()
        item_html = self.render_comment(comment=comment, request=self.request)
        return JsonResponse(self.response('Comment was successfully edited', item_html, True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response('Comment was not edited', item_html, False))
