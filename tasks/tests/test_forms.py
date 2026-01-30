from datetime import timedelta

from django.test import TestCase, RequestFactory
from django.utils import timezone

from tasks.forms import TaskCreateForm, TaskCommentForm, TaskUpdateForm, TaskResultForm
from users.models import User, Company


class TaskCreateFormTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(name="Acme")
        self.user = User.objects.create_user(username='creator', password='pass', company=self.company)
        self.assignee = User.objects.create_user(username='assignee', password='pass', company=self.company)

    def test_create_task(self):
        request = self.factory.get("/")
        request.user = self.user
        form_data = {'name': 'Task title',
                     'description': 'Task description',
                     'assignee': self.assignee.id,
                     'priority': 'MEDIUM',
                     'deadline': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')}
        form = TaskCreateForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())

    def test_create_task_invalid_deadline(self):
        request = self.factory.get("/")
        request.user = self.user
        form_data = {'name': 'Task title',
                     'description': 'Task description',
                     'assignee': self.assignee.id,
                     'priority': 'MEDIUM',
                     'deadline': (timezone.now() - timedelta(days=400)).strftime('%Y-%m-%dT%H:%M')}
        form = TaskCreateForm(data=form_data, request=request)
        self.assertFalse(form.is_valid())


class CommentFormTestCase(TestCase):
    def test_create_comment(self):
        form_data = {'text': 'Comment for the test task'}
        form = TaskCommentForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_comment_with_invalid_text(self):
        form_data = {'text': '##'}
        form = TaskCommentForm(data=form_data)
        self.assertFalse(form.is_valid())


class TaskResultFormTestCase(TestCase):
    def test_create_result(self):
        form_data = {'message': 'Result message'}
        form = TaskResultForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_create_result_invalid(self):
        form_data = {'message': 'a'}
        form = TaskResultForm(data=form_data)
        self.assertFalse(form.is_valid())


class TaskUpdateFormTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.company = Company.objects.create(name="Acme")
        self.user = User.objects.create_user(username='creator', password='pass', company=self.company)
        self.assignee = User.objects.create_user(username='assignee', password='pass', company=self.company)

    def test_update_task(self):
        request = self.factory.get("/")
        request.user = self.user
        form_data = {'name': 'Updated title',
                     'description': 'Updated description',
                     'assignee': self.assignee.id,
                     'priority': 'HIGH',
                     'deadline': (timezone.now() + timedelta(days=1)).strftime('%Y-%m-%dT%H:%M')}
        form = TaskUpdateForm(data=form_data, request=request)
        self.assertTrue(form.is_valid())
