from .add_task_view import AddTaskView
from .delete_task_view import DeleteTaskView
from .task_change_status_view import TaskChangeStatusView
from .task_update_info_view import TaskUpdateInfoView
from .task_add_result_view import TaskAddResultView
from .task_add_comment_view import TaskAddCommentView
from .task_delete_comment_view import TaskDeleteCommentView
from .task_edit_comment_view import TaskEditCommentView
from .task_kanban_list_view import TaskKanbanListView
from .task_kanban_move_view import TaskKanbanMoveView
from .task_detail_view import TaskDetailView

__all__ = [
    "AddTaskView",
    "DeleteTaskView",
    "TaskChangeStatusView",
    "TaskUpdateInfoView",
    "TaskAddResultView",
    "TaskAddCommentView",
    "TaskDeleteCommentView",
    "TaskEditCommentView",
    "TaskKanbanListView",
    "TaskKanbanMoveView",
    "TaskDetailView",
]
