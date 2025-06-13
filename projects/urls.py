from django.urls import path
from .views import AddProjectView, DeleteProjectView, UpdateProjectView

app_name = 'projects'

urlpatterns = [
    path('project-add/', AddProjectView.as_view(), name='add_proj'),
    path('project-delete/', DeleteProjectView.as_view(), name='del_proj'),
    path('project-edit/', UpdateProjectView.as_view(), name='edit_proj'),
]