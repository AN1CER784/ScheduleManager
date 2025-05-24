from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from schedule.forms import TaskCreateForm, TaskCompleteForm, TaskIncompleteForm, TaskCommentForm
from schedule.models import Task, TaskComment


class UserScheduleAddTask(LoginRequiredMixin, View):
    def post(self, request):
        form = TaskCreateForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = self.request.user
            task.save()
            item_html = render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': 'InProgress'},
                                    request=request)
            return JsonResponse({'success': True, 'message': 'Task was successfully added', 'item_html': item_html})
        errors_html = render_to_string('schedule/includes/form_errors.html', context={'form': form}, request=request)
        return JsonResponse({'success': False, 'message': 'Task was\'nt added', 'errors_html': errors_html})


class UserScheduleDeleteTask(LoginRequiredMixin, View):
    def post(self, request):
        task_id = request.POST.get('task_id')
        Task.objects.get(id=task_id).delete()
        item_html = render_to_string('schedule/includes/task_card.html', context={'task_id': task_id}, request=request)
        return JsonResponse({'success': True, 'message': 'Task was deleted', 'item_html': item_html})


class UserScheduleCompleteTask(LoginRequiredMixin, View):
    def post(self, request):
        task = Task.objects.get(id=request.POST.get('task_id'))
        form = TaskCompleteForm(request.POST, instance=task)
        form.save()
        item_html = render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': 'Done'},
                                request=request)
        return JsonResponse({'success': True, 'message': 'Task was successfully completed', 'item_html': item_html})


class UserScheduleIncompleteTask(LoginRequiredMixin, View):
    def post(self, request):
        task = Task.objects.get(id=request.POST.get('task_id'))
        form = TaskIncompleteForm(request.POST, instance=task)
        form.save()
        item_html = render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': 'InProgress'},
                                request=request)
        return JsonResponse({'success': True, 'message': 'Task was successfully incompleted', 'item_html': item_html})


class UserUpdateProgressTask(LoginRequiredMixin, View):
    def post(self, request):
        task = Task.objects.get(id=request.POST.get('task_id'))
        task.complete_percentage = int(request.POST.get('complete_percentage'))
        task.save()
        item_html = render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': 'InProgress'},
                                request=request)
        return JsonResponse({'success': True, 'message': 'Task was successfully updated', 'item_html': item_html})


class UserScheduleAddComment(LoginRequiredMixin, View):
    def post(self, request):
        task = Task.objects.get(id=request.POST.get('task_id'))
        form = TaskCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.save()
            item_html = render_to_string('schedule/includes/comment_item.html', context={'comment': comment},
                                         request=request)
            divider_html = render_to_string('schedule/includes/comment_divider.html', {
                'comment_date': comment.created_date
            }, request=request)
            return JsonResponse({'success': True, 'message': 'Comment was successfully added', 'item_html': item_html,
                                 'divider_html': divider_html, 'comment_date': comment.created_date})
        errors_html = render_to_string('schedule/includes/form_errors.html', context={'form': form}, request=request)
        return JsonResponse({'success': False, 'message': 'Comment was\'nt added', 'errors_html': errors_html})


class UserScheduleDeleteComment(LoginRequiredMixin, View):
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        TaskComment.objects.get(id=comment_id).delete()
        item_html = render_to_string('schedule/includes/comment_item.html', context={'comment_id': comment_id},
                                request=request)
        return JsonResponse({'success': True, 'message': 'Task was deleted', 'html': item_html})


class UserScheduleEditComment(LoginRequiredMixin, View):
    def post(self, request):
        comment_id = request.POST.get('comment_id')
        comment = TaskComment.objects.get(id=comment_id)
        form = TaskCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            item_html = render_to_string('schedule/includes/comment_item.html', context={'comment': comment},
                                         request=request)
            return JsonResponse({'success': True, 'message': 'Comment was successfully edited', 'item_html': item_html})
        errors_html = render_to_string('schedule/includes/form_errors.html', context={'form': form}, request=request)
        return JsonResponse({'success': False, 'message': 'Comment was\'nt edited', 'errors_html': errors_html})
