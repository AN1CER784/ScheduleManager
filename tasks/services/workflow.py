from django.utils import timezone

from tasks.models import Task


ALLOWED_STATUS_TRANSITIONS = {
    Task.Status.NEW: {Task.Status.IN_PROGRESS: "assignee"},
    Task.Status.IN_PROGRESS: {Task.Status.ON_REVIEW: "assignee"},
    Task.Status.ON_REVIEW: {Task.Status.IN_PROGRESS: "creator", Task.Status.DONE: "creator"},
}


class TaskStatusError(ValueError):
    pass


def can_transition(task: Task, user, new_status: str) -> bool:
    """????????? ????? ???????? ???????? ??? ??????????? ?? ?????."""
    return new_status in Task.Status.values


def transition_task_status(task: Task, user, new_status: str) -> str:
    """?????? ?????? ??????; ??? ?????? ?? DONE ??????? completed_at."""
    if not can_transition(task, user, new_status):
        raise TaskStatusError("Transition not allowed")
    old_status = task.status
    if new_status == old_status:
        return old_status
    task.status = new_status
    if new_status == Task.Status.DONE:
        task.completed_at = timezone.now()
    elif old_status == Task.Status.DONE:
        task.completed_at = None
    task.save(update_fields=["status", "completed_at"])
    return old_status
