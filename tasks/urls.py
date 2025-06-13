from django.urls import path
from .views import AddTaskView, DeleteTaskView, CompleteTaskView, IncompleteTaskView, \
    TaskAddCommentView, TaskDeleteCommentView, TaskUpdateProgressView, TaskEditCommentView, TaskUpdateInfoView

app_name = 'tasks'

urlpatterns = [
    path('task-add/', AddTaskView.as_view(), name='add_task'),
    path('task-del/', DeleteTaskView.as_view(), name='del_task'),
    path('task-complete/', CompleteTaskView.as_view(), name='complete_task'),
    path('task-incomplete/', IncompleteTaskView.as_view(), name='incomplete_task'),
    path('task-update-progress/', TaskUpdateProgressView.as_view(), name='task_update_progress'),
    path('task-update-info/', TaskUpdateInfoView.as_view(), name='task_update_info'),
    path('add-comment/', TaskAddCommentView.as_view(), name='add_comment'),
    path('edit-comment/', TaskEditCommentView.as_view(), name='edit_comment'),
    path('del-comment/', TaskDeleteCommentView.as_view(), name='del_comment'),
]