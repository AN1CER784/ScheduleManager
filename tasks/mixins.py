from django.template.loader import render_to_string

from common.mixins import CommonFormMixin
from projects.models import Project
from tasks.models import Task, TaskComment, TaskResult, TaskChangeLog


class TasksMixin(CommonFormMixin):
    @staticmethod
    def render_task(request, task: Task, project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/kanban_card.html',
                                context={'task': task, 'project': project},
                                request=request)

    @staticmethod
    def render_task_card(request, task: Task, project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/kanban_card.html',
                                context={'task': task, 'project': project},
                                request=request)

    @staticmethod
    def render_task_detail(request, task: Task, project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/task_detail.html',
                                context={'task': task, 'project': project,
                                         'assignees': request.user.company.users.all()},
                                request=request)

    @staticmethod
    def render_comment(request, comment: TaskComment, project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/comment_item.html',
                                context={'comment': comment, 'project': project}, request=request)

    @staticmethod
    def render_result(request, result: TaskResult, project: Project | None = None) -> str:
        return render_to_string(template_name='tasks/includes/result_item.html',
                                context={'result': result, 'project': project}, request=request)

    @staticmethod
    def render_change_log(request, entry: TaskChangeLog) -> str:
        return render_to_string(template_name='tasks/includes/change_log_item.html',
                                context={'entry': entry}, request=request)

    @staticmethod
    def get_task(request) -> Task | None:
        """???????? ?????? ?? id ? ????????? ????????, ?????????? None ???? ?? ???????."""
        return (Task.objects
                .select_related('project', 'assignee', 'creator')
                .filter(id=request.POST.get('task_id'), project__company=request.user.company)
                .first())

    @staticmethod
    def get_task_from_id(task_id, request) -> Task | None:
        """???????? ?????? ?? id (?? ?????????) ? ????????? ????????, ?????????? None ???? ?? ???????."""
        return (Task.objects
                .select_related('project', 'assignee', 'creator')
                .filter(id=task_id, project__company=request.user.company)
                .first())

    @staticmethod
    def get_comment(request) -> TaskComment | None:
        """???????? ??????????? ?? id ? ????????? ????????, ?????????? None ???? ?? ??????."""
        comment_id = request.POST.get('comment_id')
        if not comment_id:
            return None
        return (TaskComment.objects
                .select_related('task', 'task__project')
                .filter(id=comment_id, task__project__company=request.user.company)
                .first())

    @staticmethod
    def get_result(request) -> TaskResult | None:
        """???????? ????????? ?? id ? ????????? ????????, ?????????? None ???? ?? ??????."""
        result_id = request.POST.get('result_id')
        if not result_id:
            return None
        return (TaskResult.objects
                .select_related('task', 'task__project')
                .filter(id=result_id, task__project__company=request.user.company)
                .first())
