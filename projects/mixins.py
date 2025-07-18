from django.template.loader import render_to_string

from common.mixins import CommonFormMixin
from projects.models import Project


class ProjectMixin(CommonFormMixin):
    @staticmethod
    def render_project(request, project: Project) -> str:
        return render_to_string('projects/includes/project_item.html', context={'project': project}, request=request)

    @staticmethod
    def get_project(project_id: int, user_id: int | None = None, session_key: str | None = None) -> Project:
        if user_id is None:
            queryset = Project.objects.filter(session_key=session_key)
        else:
            queryset = Project.objects.filter(user_id=user_id)
        return queryset.get(id=project_id)
