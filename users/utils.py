from projects.models import Project
from users.models import User


def update_projects_user(session_key: str, user_obj: User):
    if session_key:
        Project.objects.filter(session_key=session_key).update(user=user_obj)
