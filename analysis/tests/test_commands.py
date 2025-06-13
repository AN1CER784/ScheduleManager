from datetime import datetime, timedelta

from django.test import TestCase

from projects.models import Project
from tasks.models import Task
from users.models import User


class MakeSummaryCommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        self.task1 = Task.objects.create(name='Test task 1',
                                         description='Description for the test task',
                                         start_datetime=datetime.now(),
                                         due_datetime=datetime.now() + timedelta(days=1),
                                         is_completed=False,
                                         project=self.project)
        self.task2 = Task.objects.create(name='Test task 2',
                                         description='Description for the test task',
                                         start_datetime=datetime.now(),
                                         due_datetime=datetime.now() + timedelta(days=1),
                                         is_completed=False,
                                         project=self.project)
        self.task3 = Task.objects.create(name='Test task 3',
                                         description='Description for the test task',
                                         start_datetime=datetime.now(),
                                         due_datetime=datetime.now() + timedelta(days=1),
                                         is_completed=False,
                                         project=self.project)

    def test_make_day_summary(self):
        from analysis.management.commands.make_day_summary import Command
        command = Command()
        command.handle(period=1)

    def test_make_week_summary(self):
        from analysis.management.commands.make_week_summary import Command
        command = Command()
        command.handle(period=7)
