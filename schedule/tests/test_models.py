from datetime import datetime, timedelta

from django.test import TestCase

from schedule.models import Task
from users.models import User


class TaskModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_date=datetime.now().date(),
                                        start_time=datetime.now().time(),
                                        due_date=datetime.now().date() + timedelta(days=1),
                                        due_time=datetime.now().time(),
                                        user=self.user,
                                        complete_percentage=5,
                                        complete_datetime=None,
                                        is_completed=False)

    def test_task_model(self):
        self.assertEqual(self.task.name, 'Title for the test task')
        self.assertEqual(self.task.description, 'Description for the test task')
        self.assertEqual(self.task.start_date, datetime.now().date())
        self.assertEqual(self.task.start_time, datetime.now().time())
        self.assertEqual(self.task.due_date, datetime.now().date() + timedelta(days=1))
        self.assertEqual(self.task.due_time, datetime.now().time())
        self.assertEqual(self.task.user, self.user)
        self.assertEqual(self.task.complete_percentage, 5)
        self.assertEqual(self.task.complete_datetime, None)
        self.assertEqual(self.task.is_completed, False)

    def test_complete_task(self):
        self.task.complete_percentage = 100
        self.task.save()
        self.assertEqual(self.task.complete_percentage, 100)
        self.assertEqual(self.task.is_completed, True)
        self.assertIsNotNone(self.task.complete_datetime)

    def test_incomplete_task(self):
        self.test_complete_task()
        self.task.complete_percentage = 5
        self.task.save()
        self.assertEqual(self.task.complete_percentage, 5)
        self.assertEqual(self.task.is_completed, False)
        self.assertIsNone(self.task.complete_datetime)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_date=datetime.now().date(),
                                        start_time=datetime.now().time(),
                                        due_date=datetime.now().date() + timedelta(days=1),
                                        due_time=datetime.now().time(),
                                        user=self.user,
                                        complete_percentage=5,
                                        complete_datetime=None,
                                        is_completed=False)
        self.comment = self.task.comments.create(text='Test comment', task=self.task)

    def test_comment_model(self):
        self.assertEqual(self.comment.text, 'Test comment')
        self.assertEqual(self.comment.task, self.task)
        self.assertIsNotNone(self.comment.created_date)
        self.assertIsNotNone(self.comment.created_time)
