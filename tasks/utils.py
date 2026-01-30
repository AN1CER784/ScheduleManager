from typing import Any

from tasks.models import Task, TaskChangeLog


def log_task_changes(task: Task, user, changes: dict[str, tuple[Any, Any]]) -> None:
    entries = []
    for field_name, (old_value, new_value) in changes.items():
        if old_value == new_value:
            continue
        entries.append(TaskChangeLog(
            task=task,
            changed_by=user,
            field_name=field_name,
            old_value=str(old_value) if old_value is not None else None,
            new_value=str(new_value) if new_value is not None else None,
        ))
    if entries:
        TaskChangeLog.objects.bulk_create(entries)
