from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.mixins import JsonFormMixin
from projects.forms import AddProjectForm
from projects.mixins import ProjectMixin


class UpdateProjectView(LoginRequiredMixin, ProjectMixin, JsonFormMixin, View):
    form_class = AddProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_project(project_id=self.request.POST.get('project_id'), user=self.request.user)
        return kwargs

    def form_valid(self, form):
        project = form.save()
        item_html = self.render_project(request=self.request, project=project)
        return JsonResponse(self.response(_('Project was successfully edited'), item_html, True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(_('Project was not edited'), item_html, False))
