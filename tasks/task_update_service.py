from tasks.models import TaskProgress


def create_progress(task):
    TaskProgress.objects.create(task=task)


def create_task_with_progress(task):
    task.save()
    create_progress(task=task)


def update_progress(progress, percentage):
    progress.percentage = percentage
    progress.save()

    task = progress.task
    new_status = (percentage == 100)
    if task.is_completed != new_status:
        task.is_completed = new_status
        task.save()


def add_comment(task, comment):
    comment.task = task
    comment.save()
    return comment
