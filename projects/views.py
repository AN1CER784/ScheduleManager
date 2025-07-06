from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views import View

from common.common_services import delete_object
from common.mixins import JsonFormMixin, SessionMixin
from projects.forms import AddProjectForm
from projects.mixins import ProjectMixin


class AddProjectView(JsonFormMixin, ProjectMixin, SessionMixin, View):
    form_class = AddProjectForm

    def form_valid(self, form):
        project = self.assign_owner(instance=form.save(commit=False))
        item_html = self.render_project(request=self.request, project=project)
        return JsonResponse(self.response(_('Project was successfully created'), item_html, True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(_('Error creating project'), item_html, False))


class DeleteProjectView(ProjectMixin, View):
    def post(self, request, *args, **kwargs):
        project = self.get_project(user_id=request.user.id, project_id=request.POST.get('project_id'),
                                   session_key=self.request.session.session_key)
        item_html = self.render_project(request=request, project=project)
        delete_object(model_object=project)
        return JsonResponse(self.response(_('Project was successfully deleted'), item_html, True))


class UpdateProjectView(ProjectMixin, JsonFormMixin, View):
    form_class = AddProjectForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.get_project(user_id=self.request.user.id,
                                              project_id=self.request.POST.get('project_id'),
                                              session_key=self.request.session.session_key)
        return kwargs

    def form_valid(self, form):
        project = form.save()
        item_html = self.render_project(request=self.request, project=project)
        return JsonResponse(self.response(_('Project was successfully edited'), item_html, True))

    def form_invalid(self, form):
        item_html = self.render_errors(form=form, request=self.request)
        return JsonResponse(self.response(_('Project was not edited'), item_html, False))
