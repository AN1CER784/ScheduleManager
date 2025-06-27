from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from projects.models import Project
from analysis.notifications import WeekReportNotificationBuilder, DayTaskNotificationBuilder, DayTaskNotificationFetcher
from tasks.models import Task
from users.models import User


class DayTasksNotificationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX', email='testmail@mail.com')
        project = Project.objects.create(name='Test Project', user=self.user)
        Task.objects.create(name='Title for the test task',
                            description='Description for the test task',
                            start_datetime=datetime.now() - timedelta(days=4),
                            due_datetime=datetime.now() - timedelta(days=3),
                            is_completed=False,
                            project=project)

    def test_tasks_fetcher(self):
        fetcher = DayTaskNotificationFetcher()
        tasks = fetcher.fetch(self.user)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].name, 'Title for the test task')
        self.assertEqual(tasks[0].project.name, 'Test Project')

    @patch('analysis.notifications.get_or_create_report')
    def test_tasks_builder(self, mock_get_or_create_report):
        tasks = Task.objects.all()
        builder = DayTaskNotificationBuilder()
        mail_dict = builder.build(self.user, tasks)
        subject, message, recipient_list, html_message = mail_dict
        self.assertEqual(subject, 'Day analysis report')
        self.assertIn('Your Day Productivity Report', message)
        self.assertEqual(recipient_list, ['testmail@mail.com'])
        self.assertEqual(mock_get_or_create_report.call_count, 1)



class WeekReportNotificationsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX', email='XXXXXXXXXXXXXXXXX')
        project = Project.objects.create(name='Test Project', user=self.user)
        Task.objects.create(name='Title for the test task',
                            description='Description for the test task',
                            start_datetime=datetime.now() - timedelta(days=4),
                            due_datetime=datetime.now() - timedelta(days=3),
                            is_completed=False,
                            project=project)

    @patch('analysis.notifications.get_or_create_report')
    def test_week_report_builder(self, mock_get_or_create_report):
        builder = WeekReportNotificationBuilder()
        mail_dict = builder.build(self.user)
        subject, message, recipient_list, html_message = mail_dict
        self.assertEqual(subject, 'Week analysis report')
        self.assertIn('Your Week Productivity Report', message)
        self.assertEqual(recipient_list, ['XXXXXXXXXXXXXXXXX'])
        self.assertEqual(mock_get_or_create_report.call_count, 1)


