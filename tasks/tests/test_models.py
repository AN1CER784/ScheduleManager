from datetime import datetime, timedelta

from django.test import TestCase

from projects.models import Project
from tasks.models import Task, TaskProgress
from tasks.progress_service import update_progress
from users.models import User


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        TaskProgress.objects.create(task=self.task)

    def test_task_model(self):
        self.assertEqual(self.task.name, 'Title for the test task')
        self.assertEqual(self.task.description, 'Description for the test task')
        self.assertEqual((self.task.due_datetime - self.task.start_datetime).days, 1)
        self.assertEqual(self.task.project, self.project)
        self.assertEqual(self.task.progress.percentage, 5)
        self.assertEqual(self.task.is_completed, False)

    def test_complete_task(self):
        update_progress(self.task.progress, 100)
        self.task.progress.save()
        self.assertEqual(self.task.is_completed, True)

    def test_incomplete_task(self):
        self.test_complete_task()
        update_progress(self.task.progress, 5)
        self.task.progress.save()
        self.assertEqual(self.task.progress.percentage, 5)
        self.assertEqual(self.task.is_completed, False)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        self.comment = self.task.comments.create(text='Test comment', task=self.task)

    def test_comment_model(self):
        self.assertEqual(self.comment.text, 'Test comment')
        self.assertEqual(self.comment.task, self.task)
        self.assertIsNotNone(self.comment.created_date)
        self.assertIsNotNone(self.comment.created_time)



