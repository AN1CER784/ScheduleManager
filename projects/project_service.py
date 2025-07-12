from projects.models import Project


def delete_project(project: Project) -> None:
    project.delete()
