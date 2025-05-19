from django.urls import path
from .views import UserScheduleAddTask, UserScheduleDeleteTask, UserScheduleCompleteTask, UserScheduleIncompleteTask, \
    UserScheduleAddComment, UserScheduleDeleteComment, UserUpdateProgressTask

app_name = 'schedule'

urlpatterns = [
    path('task-add/', UserScheduleAddTask.as_view(), name='add_task'),
    path('task-del/', UserScheduleDeleteTask.as_view(), name='del_task'),
    path('task-complete/', UserScheduleCompleteTask.as_view(), name='complete_task'),
    path('task-incomplete/', UserScheduleIncompleteTask.as_view(), name='incomplete_task'),
    path('task-update-progress/', UserUpdateProgressTask.as_view(), name='task_update_progress'),
    path('add-comment/', UserScheduleAddComment.as_view(), name='add_comment'),
    path('del-comment/', UserScheduleDeleteComment.as_view(), name='del_comment'),
]