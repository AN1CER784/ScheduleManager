from django.template.loader import render_to_string

from common.mixins import CommonFormMixin
from projects.models import Project


class ProjectMixin(CommonFormMixin):
    @staticmethod
    def render_project(request, project: Project) -> str:
        return render_to_string('projects/includes/project_item.html', context={'project': project}, request=request)

    @staticmethod
    def get_project(project_id: int, user) -> Project:
        return Project.objects.get(id=project_id, company=user.company)
