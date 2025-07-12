from tasks.models import TaskProgress, Task, TaskComment


def create_progress(task: Task):
    TaskProgress.objects.create(task=task)


def create_task_with_progress(task: Task):
    task.save()
    create_progress(task=task)


def update_progress(progress: TaskProgress, percentage: int) -> None:
    progress.percentage = percentage
    progress.save()
    task = progress.task
    new_status = (percentage == 100)
    if task.is_completed != new_status:
        task.is_completed = new_status
        task.save()


def add_comment(task: Task, comment: TaskComment) -> TaskComment:
    comment.task = task
    comment.save()
    return comment
