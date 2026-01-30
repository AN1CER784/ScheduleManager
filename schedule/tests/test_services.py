from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from projects.models import Project
from schedule.calendar_builder_service import TaskCalendarBuilder
from tasks.models import Task
from users.models import Company, User


class TaskCalendarBuilderTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Acme")
        self.user = User.objects.create_user(username='user', password='pass', company=self.company)

    def test_calendar_builder_with_no_tasks(self):
        task_calendar_builder = TaskCalendarBuilder(None)
        task_calendar_builder.build()
        self.assertEqual(len(task_calendar_builder.get_months_list), 1)
        self.assertEqual(task_calendar_builder.get_current_index, 1)
        self.assertIsNone(task_calendar_builder._tasks)
        self.assertIsNone(task_calendar_builder._min_date)
        self.assertIsNone(task_calendar_builder._max_date)

    def test_calendar_builder_with_tasks(self):
        project = Project.objects.create(name="Test Project", company=self.company, created_by=self.user)
        task1 = Task.objects.create(name='Test Task 1',
                                    description='Description for the test task',
                                    deadline=timezone.now() + timedelta(days=3),
                                    project=project,
                                    creator=self.user,
                                    assignee=self.user)

        task2 = Task.objects.create(name='Test Task 2',
                                    description='Description for the test task',
                                    deadline=timezone.now() + timedelta(days=21),
                                    project=project,
                                    creator=self.user,
                                    assignee=self.user)
        task3 = Task.objects.create(name='Test Task 3',
                                    description='Description for the test task',
                                    deadline=timezone.now() + timedelta(days=34),
                                    project=project,
                                    creator=self.user,
                                    assignee=self.user)
        task4 = Task.objects.create(name='Test Task 4',
                                    description='Description for the test task',
                                    deadline=timezone.now() + timedelta(days=60),
                                    project=project,
                                    creator=self.user,
                                    assignee=self.user)
        tasks = [task1, task2, task3, task4]
        task_calendar_builder = TaskCalendarBuilder(tasks)
        task_calendar_builder.build()
        self.assertEqual(task_calendar_builder._tasks, tasks)
        self.assertEqual(task_calendar_builder._min_date, timezone.now().date())
        self.assertEqual(task_calendar_builder._max_date, timezone.now().date() + timedelta(days=60))
        self.assertEqual(task_calendar_builder.get_current_index, 1)
        self.assertEqual(len(task_calendar_builder.get_months_list), 3)
