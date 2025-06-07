from schedule.models import Task


def update_task_user(session_key, user_obj):
    if session_key:
        Task.objects.filter(session_key=session_key).update(user=user_obj)

