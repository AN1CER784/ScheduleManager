from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View

from schedule.forms import TaskForm, TaskCompleteForm
from schedule.models import Task


class UserScheduleAddTask(LoginRequiredMixin, View):
    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = self.request.user
            task.save()
            html = render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': 'pending'}, request=request)
            return JsonResponse({'success': True, 'message': 'Task was successfully added', 'html': html})
        errors_html = render_to_string('schedule/includes/form_errors.html', context={'form': form}, request=request)
        return JsonResponse({'success': False, 'message': 'Task was\'nt added', 'errors_html': errors_html})


class UserScheduleDeleteTask(LoginRequiredMixin, View):
    def post(self, request):
        task_id = request.POST.get('task_id')
        Task.objects.get(id=task_id).delete()
        html = render_to_string('schedule/includes/task_card.html', context={'task_id': task_id}, request=request)
        return JsonResponse({'success': True, 'message': 'Task was deleted', 'html': html})


class UserScheduleCompleteTask(LoginRequiredMixin, View):
    def post(self, request):
        form = TaskCompleteForm(request.POST)
        if form.is_valid():
            task = Task.objects.get(id=request.POST.get('task_id'))
            task.status = form.cleaned_data['status']
            task.status_comment = form.cleaned_data['status_comment']
            task.save()
            status_dict = {True: 'Completed', False: 'Could not complete'}
            html = render_to_string('schedule/includes/task_card.html', context={'task': task, 'type': 'done', 'status_dict': status_dict}, request=request)
            return JsonResponse({'success': True, 'message': 'Task was successfully completed', 'html': html})
        errors_html = render_to_string('schedule/includes/form_errors.html', context={'form': form}, request=request)
        return JsonResponse({'success': False, 'message': 'Task was\'nt completed', 'errors_html': errors_html})

