from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from projects.models import Project
from tasks.models import Task, TaskResult, TaskChangeLog
from users.models import User, Company


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Acme")
        self.creator = User.objects.create_user(username='creator', password='pass', company=self.company)
        self.assignee = User.objects.create_user(username='assignee', password='pass', company=self.company)
        self.project = Project.objects.create(name='Test Project', company=self.company, created_by=self.creator)
        self.project.participants.add(self.creator, self.assignee)

    def test_task_model_defaults(self):
        task = Task.objects.create(name='Title for task',
                                   description='Description for task',
                                   deadline=timezone.now() + timedelta(days=1),
                                   project=self.project,
                                   creator=self.creator,
                                   assignee=self.assignee)
        self.assertEqual(task.status, Task.Status.NEW)
        self.assertEqual(task.priority, Task.Priority.MEDIUM)
        self.assertFalse(task.is_done)
        self.assertEqual(task.position, 0)

    def test_task_result_model(self):
        task = Task.objects.create(name='Title for task',
                                   project=self.project,
                                   creator=self.creator,
                                   assignee=self.assignee)
        result = TaskResult.objects.create(task=task, author=self.assignee, message="Done")
        self.assertEqual(result.task, task)
        self.assertEqual(result.author, self.assignee)

    def test_task_change_log_model(self):
        task = Task.objects.create(name='Title for task',
                                   project=self.project,
                                   creator=self.creator,
                                   assignee=self.assignee)
        entry = TaskChangeLog.objects.create(task=task, changed_by=self.creator,
                                             field_name="name", old_value="Old", new_value="New")
        self.assertEqual(entry.task, task)
        self.assertEqual(entry.changed_by, self.creator)

    def test_task_overdue_property(self):
        task = Task.objects.create(name='Overdue',
                                   project=self.project,
                                   creator=self.creator,
                                   assignee=self.assignee,
                                   deadline=timezone.now() - timedelta(days=1))
        self.assertTrue(task.is_overdue)
