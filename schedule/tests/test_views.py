from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from schedule.models import Task
from users.models import User


class AddTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')

    def test_add_task(self):
        response = self.client.post(reverse('schedule:add_task'), {
            'name': 'Title for the test task',
            'description': 'Description for the test task',
            'start_date': datetime.now().date(),
            'start_time': datetime.now().time(),
            'due_date': datetime.now().date() + timedelta(days=1),
            'due_time': datetime.now().time(),
            'user': self.user.id
        })

        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Title for the test task')
        self.assertEqual(task.description, 'Description for the test task')
        self.assertEqual(task.start_date, datetime.now().date())
        self.assertEqual(task.due_date, datetime.now().date() + timedelta(days=1))
        self.assertEqual(task.user, self.user)
        self.assertEqual(task.complete_percentage, 5)
        self.assertEqual(task.complete_datetime, None)
        self.assertEqual(task.is_completed, False)

    def test_add_task_invalid_data(self):
        response = self.client.post(reverse('schedule:add_task'), {
            'name': '2131313',
            'description': '32142154435435345',
            'start_date': datetime.now().date(),
            'start_time': datetime.now().time(),
            'due_date': datetime.now().date() - timedelta(days=1),
            'due_time': datetime.now().time(),
            'user': self.user.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class DeleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(
            name='Title for the test task',
            description='Description for the test task',
            start_date=datetime.now().date(),
            start_time=datetime.now().time(),
            due_date=datetime.now().date() + timedelta(days=1),
            due_time=datetime.now().time(),
            user=self.user,
            complete_percentage=5,
            complete_datetime=None,
            is_completed=False
        )

    def test_delete_task(self):
        response = self.client.post(reverse('schedule:del_task'), {'task_id': self.task.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class CompleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(
            name='Title for the test task',
            description='Description for the test task',
            start_date=datetime.now().date(),
            start_time=datetime.now().time(),
            due_date=datetime.now().date() + timedelta(days=1),
            due_time=datetime.now().time(),
            user=self.user,
            complete_percentage=5,
            complete_datetime=None,
            is_completed=False
        )

    def test_complete_task(self):
        response = self.client.post(reverse('schedule:complete_task'), {'task_id': self.task.id})
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.complete_percentage, 100)
        self.assertEqual(task.is_completed, True)
        self.assertIsNotNone(task.complete_datetime)

    def test_complete_task_by_progress(self):
        response = self.client.post(reverse('schedule:task_update_progress'), {'task_id': self.task.id, 'complete_percentage': 100})
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.complete_percentage, 100)
        self.assertEqual(task.is_completed, True)
        self.assertIsNotNone(task.complete_datetime)


class IncompleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(
            name='Title for the test task',
            description='Description for the test task',
            start_date=datetime.now().date(),
            start_time=datetime.now().time(),
            due_date=datetime.now().date() + timedelta(days=1),
            due_time=datetime.now().time(),
            user=self.user,
            complete_percentage=100,
            complete_datetime=timezone.now(),
            is_completed=True
        )

    def test_incomplete_task(self):
        response = self.client.post(reverse('schedule:incomplete_task'), {'task_id': self.task.id})
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.complete_percentage, 5)
        self.assertEqual(task.is_completed, False)
        self.assertIsNone(task.complete_datetime)


class ChangeProgressTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(
            name='Title for the test task',
            description='Description for the test task',
            start_date=datetime.now().date(),
            start_time=datetime.now().time(),
            due_date=datetime.now().date() + timedelta(days=1),
            due_time=datetime.now().time(),
            user=self.user,
            complete_percentage=5,
            complete_datetime=None,
            is_completed=False
        )

    def test_change_progress_task(self):
        response = self.client.post(reverse('schedule:task_update_progress'), {
            'task_id': self.task.id,
            'complete_percentage': 50
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.complete_percentage, 50)


class AddCommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.task = Task.objects.create(
            name='Title for the test task',
            description='Description for the test task',
            start_date=datetime.now().date(),
            start_time=datetime.now().time(),
            due_date=datetime.now().date() + timedelta(days=1),
            due_time=datetime.now().time(),
            user=self.user,
            complete_percentage=5,
            complete_datetime=None,
            is_completed=False
        )

    def test_add_comment(self):
        response = self.client.post(reverse('schedule:add_comment'), {
            'task_id': self.task.id,
            'text': 'I did something'
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.comments.count(), 1)
        self.assertEqual(task.comments.first().text, 'I did something')

    def test_add_comment_invalid_data(self):
        response = self.client.post(reverse('schedule:add_comment'), {
            'task_id': self.task.id,
            'text': '####################'
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.comments.count(), 0)
