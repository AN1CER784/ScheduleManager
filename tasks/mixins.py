from typing import Literal

from django.template.loader import render_to_string

from common.mixins import CommonFormMixin
from projects.models import Project
from tasks.models import Task, TaskComment


class TasksMixin(CommonFormMixin):
    @staticmethod
    def render_task(request, task: Task, task_type: Literal['Done', 'InProgress'] = "InProgress",
                    project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/task_item.html',
                                context={'task': task, 'type': task_type, 'project': project},
                                request=request)

    @staticmethod
    def render_comment(request, comment: TaskComment, project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/comment_item.html',
                                context={'comment': comment, 'project': project}, request=request)

    @staticmethod
    def get_task(request) -> Task:
        return Task.objects.filter(id=request.POST.get('task_id')).select_related('progress').first()

    @staticmethod
    def get_comment(request) -> TaskComment:
        return TaskComment.objects.get(id=request.POST.get('comment_id'))
