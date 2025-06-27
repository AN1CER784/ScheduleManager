from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from analysis.models import AnalysisPrompt, AnalysisReport
from projects.models import Project
from tasks.models import Task
from users.models import User
from analysis.management.commands.make_summary import Command

class MakeSummaryCommandTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.client.login(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        AnalysisPrompt.objects.create(period=1, prompt="Test prompt for day")
        AnalysisPrompt.objects.create(period=7, prompt="Test prompt for week")
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
        self.task_ids = [self.task1.id, self.task2.id, self.task3.id]

    @patch('analysis.management.commands.make_summary.SummaryGenerator.generate_summary')
    @patch('analysis.management.commands.make_summary.get_or_create_report')
    def test_make_day_summary(self, mock_get_or_create_report, mock_generate_summary):
        mock_generate_summary.return_value = "Test summary"
        rep = AnalysisReport.objects.create(report="test_report", user=self.user, period=1, start_date=timezone.now().date(), end_date=timezone.now().date())
        mock_get_or_create_report.return_value = rep
        command = Command()
        command.handle(username=self.user.username, start_date=datetime.now().date(), end_date=datetime.now().date(), tasks_ids=self.task_ids, period=1)
        self.assertEqual(mock_generate_summary.call_count, 1)
        self.assertEqual(mock_get_or_create_report.call_count, 1)

    @patch('analysis.management.commands.make_summary.SummaryGenerator.generate_summary')
    @patch('analysis.management.commands.make_summary.get_or_create_report')
    def test_make_week_summary(self, mock_get_or_create_report, mock_generate_summary):
        mock_generate_summary.return_value = "Test summary"
        rep = AnalysisReport.objects.create(report="test_report", user=self.user, period=1,
                                            start_date=timezone.now().date(), end_date=timezone.now().date())
        mock_get_or_create_report.return_value = rep
        command = Command()
        command.handle(username=self.user.username, start_date=datetime.now().date(), end_date=datetime.now().date()-timedelta(6), tasks_ids=self.task_ids, period=7)
        self.assertEqual(mock_generate_summary.call_count, 1)
        self.assertEqual(mock_get_or_create_report.call_count, 1)
