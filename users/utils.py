from projects.models import Project

def update_projects_user(session_key, user_obj):
    if session_key:
        Project.objects.filter(session_key=session_key).update(user=user_obj)

