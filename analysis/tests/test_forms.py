from datetime import datetime, timedelta


from django.test import TestCase

from analysis.forms import GenerationForm
from projects.models import Project
from tasks.models import Task
from users.models import User


class GenerationFormTestCase(TestCase):
    def test_valid_generation_form(self):
        user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        project = Project.objects.create(name='Test Project', user=user)
        Task.objects.create(name='Test task 1',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=project)
        Task.objects.create(name='Test task 2',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=project)
        Task.objects.create(name='Test task 3',
                                         description='Description for the test task',
                                         start_datetime=datetime.now(),
                                         due_datetime=datetime.now() + timedelta(days=1),
                                         is_completed=False,
                                         project=project)
        form_data = {
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
            'period': 1,
            'username': 'XXXXXXXX',
        }
        form = GenerationForm(data=form_data, user=user)
        self.assertTrue(form.is_valid())

    def test_invalid_generation_form(self):
        user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        Project.objects.create(name='Test Project', user=user)
        form_data = {
            'start_date': datetime.now().date(),
            'end_date': datetime.now().date(),
            'period': 1,
            'username': 'XXXXXXXX',
        }
        form = GenerationForm(data=form_data, user=user)
        self.assertFalse(form.is_valid())