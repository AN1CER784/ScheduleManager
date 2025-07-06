from datetime import datetime, timedelta

from django.test import TestCase

from projects.models import Project
from schedule.calendar_builder_service import TaskCalendarBuilder


class TaskCalendarBuilderTestCase(TestCase):
    def test_calendar_builder_with_no_tasks(self):
        task_calendar_builder = TaskCalendarBuilder(None)
        task_calendar_builder.build()
        self.assertEqual(len(task_calendar_builder.get_months_list), 1)
        self.assertEqual(task_calendar_builder.get_current_index, 1)
        self.assertIsNone(task_calendar_builder._tasks)
        self.assertIsNone(task_calendar_builder._min_date)
        self.assertIsNone(task_calendar_builder._max_date)

    def test_calendar_builder_with_tasks(self):
        project = Project.objects.create(name="Test Project")
        task1 = project.tasks.create(name='Test Task 1',
                                     description='Description for the test task',
                                     start_datetime=datetime.now() + timedelta(days=1),
                                     due_datetime=datetime.now() + timedelta(days=3),
                                     is_completed=False,
                                     project=project)

        task2 = project.tasks.create(name='Test Task 2',
                                     description='Description for the test task',
                                     start_datetime=datetime.now(),
                                     due_datetime=datetime.now() + timedelta(days=21),
                                     is_completed=False,
                                     project=project)
        task3 = project.tasks.create(name='Test Task 3',
                                     description='Description for the test task',
                                     start_datetime=datetime.now(),
                                     due_datetime=datetime.now() + timedelta(days=34),
                                     is_completed=False,
                                     project=project)
        task4 = project.tasks.create(name='Test Task 4',
                                     description='Description for the test task',
                                     start_datetime=datetime.now(),
                                     due_datetime=datetime.now() + timedelta(days=60),
                                     is_completed=False,
                                     project=project)
        tasks = [task1, task2, task3, task4]
        task_calendar_builder = TaskCalendarBuilder(tasks)
        task_calendar_builder.build()
        self.assertEqual(task_calendar_builder._tasks, tasks)
        self.assertEqual(task_calendar_builder._min_date, datetime.now().date())
        self.assertEqual(task_calendar_builder._max_date, datetime.now().date() + timedelta(days=60))
        self.assertEqual(task_calendar_builder.get_current_index, 1)
        self.assertEqual(len(task_calendar_builder.get_months_list), 3)
