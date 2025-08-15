from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from projects.models import Project
from tasks.models import Task, TaskProgress
from users.models import User


class AddTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)

    def test_add_task(self):
        response = self.client.post(reverse('tasks:add_task', kwargs={"id": self.project.id}), {
            'name': 'Title for the test task',
            'description': 'Description for the test task',
            'start_date': datetime.now().date() + timedelta(days=1),
            'start_time': datetime.now().time(),
            'due_date': datetime.now().date() + timedelta(days=2),
            'due_time': datetime.now().time(),
            'project_id': self.project.id,
        })

        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Title for the test task')
        self.assertEqual(task.description, 'Description for the test task')
        self.assertEqual(task.start_datetime.date(), datetime.now().date() + timedelta(days=1))
        self.assertEqual(task.due_datetime.date(), datetime.now().date() + timedelta(days=2))
        self.assertEqual(task.is_completed, False)

    def test_add_task_invalid_data(self):
        response = self.client.post(reverse('tasks:add_task', kwargs={"id": self.project.id}), {
            'name': '2131313',
            'description': '32142154435435345',
            'start_date': datetime.now().date(),
            'start_time': datetime.now().time(),
            'due_date': datetime.now().date() - timedelta(days=1),
            'due_time': datetime.now().time(),
            'project_id': self.project.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class DeleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)

    def test_delete_task(self):
        response = self.client.post(reverse('tasks:del_task', kwargs={"id": self.project.id}), {'task_id': self.task.id})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class CompleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        TaskProgress.objects.create(task=self.task)

    def test_complete_task(self):
        response = self.client.post(reverse('tasks:complete_task', kwargs={"id": self.project.id}),
                                    {'task_id': self.task.id})
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.progress.percentage, 100)
        self.assertEqual(task.is_completed, True)

    def test_complete_task_by_progress(self):
        response = self.client.post(reverse('tasks:task_update_progress', kwargs={"id": self.project.id}),
                                    {'task_id': self.task.id, 'complete_percentage': 100})
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.progress.percentage, 100)
        self.assertEqual(task.is_completed, True)


class IncompleteTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        TaskProgress.objects.create(task=self.task)

    def test_incomplete_task(self):
        response = self.client.post(reverse('tasks:incomplete_task', kwargs={"id": self.project.id}),
                                    {'task_id': self.task.id})
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.progress.percentage, 5)
        self.assertEqual(task.is_completed, False)


class ChangeProgressTaskTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        TaskProgress.objects.create(task=self.task)

    def test_change_progress_task(self):
        response = self.client.post(reverse('tasks:task_update_progress', kwargs={"id": self.project.id}),
                                    {'task_id': self.task.id,
                                            'complete_percentage': 50
                                            })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.progress.percentage, 50)


class AddCommentTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)

    def test_add_comment(self):
        response = self.client.post(reverse('tasks:add_comment', kwargs={"id": self.project.id}),  {'task_id': self.task.id,
            'text': 'I did something'
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.comments.count(), 1)
        self.assertEqual(task.comments.first().text, 'I did something')

    def test_add_comment_invalid_data(self):
        response = self.client.post(reverse('tasks:add_comment', kwargs={"id": self.project.id}), {'task_id': self.task.id,
            'text': '####################'
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.comments.count(), 0)


class TaskUpdateInfoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task = Task.objects.create(name='Title for the test task',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)

    def test_edit_task(self):
        response = self.client.post(reverse('tasks:task_update_info', kwargs={"id": self.project.id}), {'task_id': self.task.id,
            'name': 'Title for the test task 1',
            'description': 'Description for the test task 1',
            'start_datetime': datetime.now(),
            'due_datetime': datetime.now() + timedelta(days=2),
            'project_id': self.project.id,
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Title for the test task 1')
        self.assertEqual(task.description, 'Description for the test task 1')
        self.assertEqual(task.start_datetime.date(), datetime.now().date())
        self.assertEqual(task.due_datetime.date(), datetime.now().date() + timedelta(days=2))

    def test_edit_task_invalid_data(self):
        response = self.client.post(reverse('tasks:task_update_info', kwargs={"id": self.project.id}), {'task_id': self.task.id,
            'name': 'Title for the test task',
            'description': 'Description for the test task',
            'start_datetime': datetime.now(),
            'due_datetime': datetime.now() - timedelta(days=1),
            'project_id': self.project.id,
        })
        self.assertEqual(response.status_code, 200)
        task = Task.objects.first()
        self.assertEqual(task.name, 'Title for the test task')
        self.assertEqual(task.description, 'Description for the test task')
        self.assertEqual(task.start_datetime.date(), datetime.now().date())
        self.assertEqual(task.due_datetime.date(), datetime.now().date() + timedelta(days=1))