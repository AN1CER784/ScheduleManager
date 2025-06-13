from django.template.loader import render_to_string
from common.mixins import CommonFormMixin
from projects.models import Project


class ProjectMixin(CommonFormMixin):
    def render_project(self, request, project):
        return render_to_string('projects/includes/project_item.html', context={'project': project}, request=request)

    def get_project(self, project_id, user_id=None, session_key=None):
        if user_id is None:
            queryset = Project.objects.filter(session_key=session_key)
        else:
            queryset = Project.objects.filter(user_id=user_id)
        return queryset.get(id=project_id)
