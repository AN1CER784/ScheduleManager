from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from analysis.models import AnalysisReport, AnalysisSummary, AnalysisPrompt
from analysis.tasks import make_day_report, make_week_report, make_summary
from projects.models import Project
from tasks.models import Task
from users.models import User


class CeleryTaskTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1', password='XXXX_password')
        self.user2 = User.objects.create(username='user2', password='XXXX_password')
        self.user3 = User.objects.create(username='user3', password='XXXX_password')

    @patch('common.notifications.UserNotificationManager.notify')
    def test_celery_notify_about_day_report(self, mock_notification_manager_class):
        result = make_day_report.delay()
        self.assertTrue(result.successful())
        self.assertTrue(mock_notification_manager_class.called)
        self.assertEqual(mock_notification_manager_class.call_count, 3)

    @patch('common.notifications.UserNotificationManager.notify')
    def test_celery_notify_about_week_report(self, mock_notification_manager_class):
        result = make_week_report.delay()
        self.assertTrue(result.successful())
        self.assertTrue(mock_notification_manager_class.called)
        self.assertEqual(mock_notification_manager_class.call_count, 3)

    @patch('analysis.tasks.SummaryGenerator')
    def test_make_summary(self, mock_generator):
        instance = mock_generator.return_value
        instance.generate_summary.return_value = "Test generation"
        report = AnalysisReport.objects.create(user=self.user1, period=7, start_date="2022-01-01", end_date="2022-01-07", report={"name": "test_report"})
        AnalysisPrompt.objects.create(period=7, prompt="…")
        AnalysisSummary.objects.create(report=report)
        project = Project.objects.create(user=self.user1, name="test_project")
        Task.objects.bulk_create([
            Task(id=1, project=project, name="test_task1", description="test_task1", is_completed=True, start_datetime=timezone.now(), due_datetime=timezone.now() + timedelta(1)),
            Task(id=2, project=project, name="test_task2", description="test_task2", is_completed=True, start_datetime=timezone.now(), due_datetime=timezone.now() + timedelta(1)),
            Task(id=3, project=project, name="test_task3", description="test_task3", is_completed=True, start_datetime=timezone.now(), due_datetime=timezone.now() + timedelta(1)),
        ])
        user_id, report_id, tasks_ids, period = self.user1.id, report.id, [1, 2, 3], 7
        result = make_summary.delay(user_id, report_id, tasks_ids, period)
        self.assertTrue(result.successful())
        self.assertTrue(mock_generator.called)
        self.assertEqual(mock_generator.call_count, 1)

