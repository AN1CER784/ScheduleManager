from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase

from analysis.services.reports import get_or_create_report
from projects.models import Project
from tasks.models import Task
from users.models import User
from analysis.utils import get_date_range_from_week

class ReportTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        Task.objects.create(name='Test task 1',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Test task 2',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Test task 3',
                                         description='Description for the test task',
                                         start_datetime=datetime.now(),
                                         due_datetime=datetime.now() + timedelta(days=1),
                                         is_completed=False,
                                         project=self.project)
    @patch('analysis.services.productivity_matrix.TaskAutomatonReport.generate_report')
    def test_generate_week_report(self, mock_generate_report):
        mock_generate_report.return_value = '{"mocked": "report"}'
        report = get_or_create_report(user=self.user, period=7)
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.period, 7)
        self.assertIsNotNone(report.report)

    @patch('analysis.services.productivity_matrix.TaskAutomatonReport.generate_report')
    def test_generate_day_report(self, mock_generate_report):
        mock_generate_report.return_value = '{"mocked": "report"}'
        report = get_or_create_report(user=self.user, period=1)
        self.assertEqual(report.user, self.user)
        self.assertEqual(report.period, 1)
        self.assertIsNotNone(report.report)

class DateRangeFromWeekTestCase(TestCase):
    def test_get_date_range_from_week(self):
        year_week_str = '2023-W01'
        first_day, last_day = get_date_range_from_week(year_week_str)
        self.assertEqual(first_day.weekday(), 0)
        self.assertEqual(last_day.weekday(), 6)
        self.assertEqual(first_day.strftime('%Y-%m-%d'), '2023-01-02')
        self.assertEqual(last_day.strftime('%Y-%m-%d'), '2023-01-08')