from django.urls import path
from .views import AddTaskView, DeleteTaskView, TaskChangeStatusView, TaskAddCommentView, TaskDeleteCommentView, \
    TaskEditCommentView, TaskUpdateInfoView, TaskAddResultView, TaskKanbanListView, TaskKanbanMoveView, \
    TaskDetailView

app_name = 'tasks'

urlpatterns = [
    path('task-add/', AddTaskView.as_view(), name='add_task'),
    path('task-del/', DeleteTaskView.as_view(), name='del_task'),
    path('task-change-status/', TaskChangeStatusView.as_view(), name='task_change_status'),
    path('task-update-info/', TaskUpdateInfoView.as_view(), name='task_update_info'),
    path('add-comment/', TaskAddCommentView.as_view(), name='add_comment'),
    path('edit-comment/', TaskEditCommentView.as_view(), name='edit_comment'),
    path('del-comment/', TaskDeleteCommentView.as_view(), name='del_comment'),
    path('add-result/', TaskAddResultView.as_view(), name='add_result'),
    path('kanban-list/', TaskKanbanListView.as_view(), name='kanban_list'),
    path('kanban-move/', TaskKanbanMoveView.as_view(), name='kanban_move'),
    path('task-detail/', TaskDetailView.as_view(), name='task_detail'),
]
