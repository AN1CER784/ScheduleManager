from django.urls import path
from .views import UserScheduleAddTask, UserScheduleDeleteTask, UserScheduleCompleteTask


app_name = 'schedule'

urlpatterns = [
    path('task-add/', UserScheduleAddTask.as_view(), name='add_task'),
    path('task-del/', UserScheduleDeleteTask.as_view(), name='del_task'),
    path('task-complete/', UserScheduleCompleteTask.as_view(), name='complete_task'),
]