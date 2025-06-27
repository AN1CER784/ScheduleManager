from datetime import datetime, timedelta

from django.urls import reverse
from django.test import TestCase

from analysis.models import AnalysisSummary, AnalysisReport
from projects.models import Project
from tasks.models import Task
from users.models import User

class GenerateSummaryViewTesCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        Task.objects.create(name='Title for the test task 1',
                            description='Description for the test task',
                            start_datetime=datetime.now() - timedelta(days=7),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Title for the test task 2',
                            description='Description for the test task',
                            start_datetime=datetime.now() - timedelta(days=3),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Title for the test task 3',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Title for the test task 4',
                                    description='Description for the test task',
                                    start_datetime=datetime.now(),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)

    def test_generate_summary_daily_view(self):
        self.client.login(username=self.user.username, password='XXXXXXXXXXXX')
        response = self.client.post(reverse('analysis:generate-summary'), {'period': '1', 'date': datetime.now().date()})
        self.assertEqual(response.status_code, 200)

    def test_generate_summary_weekly_view(self):
        self.client.login(username=self.user.username, password='XXXXXXXXXXXX')
        current_datetime = datetime.now().today()
        response = self.client.post(reverse('analysis:generate-summary'), {'period': '7', 'week': f"{current_datetime.year}-W{current_datetime.isocalendar()[1]}"})
        self.assertEqual(response.status_code, 200)

class DeleteSummaryViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        Task.objects.create(name='Title for the test task 1',
                            description='Description for the test task',
                            start_datetime=datetime.now() - timedelta(days=7),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Title for the test task 2',
                            description='Description for the test task',
                            start_datetime=datetime.now() - timedelta(days=3),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Title for the test task 3',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        Task.objects.create(name='Title for the test task 4',
                            description='Description for the test task',
                            start_datetime=datetime.now(),
                            due_datetime=datetime.now() + timedelta(days=1),
                            is_completed=False,
                            project=self.project)
        self.report = AnalysisReport.objects.create(user=self.user, period=1, report={"report": "Test report"}, start_date=datetime.now().date(), end_date=datetime.now().date())
        AnalysisSummary.objects.create(report=self.report , summary='Test summary')

    def test_delete_summary_view(self):
        self.client.login(username=self.user.username, password='XXXXXXXXXXXX')
        response = self.client.post(reverse('analysis:delete-summary'), {'report_id': self.report.id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(AnalysisSummary.objects.filter(report=self.report).exists())
