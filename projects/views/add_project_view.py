from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.mixins import JsonFormMixin
from projects.forms import AddProjectForm
from projects.mixins import ProjectMixin
from projects.models import Project


class AddProjectView(LoginRequiredMixin, JsonFormMixin, ProjectMixin, View):
    form_class = AddProjectForm

    def form_valid(self, form):
        project: Project = form.save(commit=False)
        project.company = self.request.user.company
        project.created_by = self.request.user
        project.save()
        project.participants.add(self.request.user)
        item_html = self.render_project(request=self.request, project=project)
        return JsonResponse(self.response(_('Project was successfully created'), item_html, True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(_('Error creating project'), item_html, False))
