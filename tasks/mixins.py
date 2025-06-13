from django.template.loader import render_to_string
from common.mixins import CommonFormMixin

from tasks.models import Task, TaskComment

class TasksMixin(CommonFormMixin):
    def render_task(self, request, task, task_type="InProgress", project=None):
        return render_to_string(template_name='tasks/includes/task_item.html', context={'task': task, 'type': task_type, 'project': project},
                                request=request)

    def render_comment(self, request, comment, project=None):
        return render_to_string(template_name='tasks/includes/comment_item.html', context={'comment': comment, 'project': project}, request=request)

    def get_task(self, request):
        return Task.objects.get(id=request.POST.get('task_id'))

    def get_comment(self, request):
        return TaskComment.objects.get(id=request.POST.get('comment_id'))


