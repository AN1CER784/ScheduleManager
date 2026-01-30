from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.utils import delete_object
from projects.mixins import ProjectMixin


class DeleteProjectView(LoginRequiredMixin, ProjectMixin, View):
    def post(self, request, *args, **kwargs):
        project = self.get_project(project_id=request.POST.get('project_id'), user=request.user)
        item_html = self.render_project(request=request, project=project)
        delete_object(model_object=project)
        return JsonResponse(self.response(_('Project was successfully deleted'), item_html, True))
