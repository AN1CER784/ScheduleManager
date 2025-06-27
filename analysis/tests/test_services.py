from datetime import datetime, timedelta

from django.test import TestCase
from projects.models import Project
from tasks.models import Task
from users.models import User
from analysis.services.summary_generator import SummaryGenerator
from analysis.services.productivity_matrix import TaskAutomatonReport

class AnalysisGeneratorTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        task1 = Task.objects.create(name='Title for the test task 1',
                                        description='Description for the test task',
                                        start_datetime=datetime.now(),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        task2 = Task.objects.create(name='Title for the test task 2',
                                    description='Description for the test task',
                                    start_datetime=datetime.now(),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)
        task3 = Task.objects.create(name='Title for the test task 3',
                                    description='Description for the test task',
                                    start_datetime=datetime.now(),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)
        task4 = Task.objects.create(name='Title for the test task 4',
                                    description='Description for the test task',
                                    start_datetime=datetime.now(),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)
        self.tasks = [task1, task2, task3, task4]

    def test_analysis_generator(self):
        prompt = "Test prompt"
        generator = SummaryGenerator(self.tasks, prompt)
        response = generator.generate_summary()
        self.assertIsNotNone(response)
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)

class TaskAutomatonReportTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='XXXXXXXX', password='XXXXXXXXXXXX')
        self.project = Project.objects.create(name='Test Project', user=self.user)
        task1 = Task.objects.create(name='Title for the test task 1',
                                        description='Description for the test task',
                                        start_datetime=datetime.now() - timedelta(days=7),
                                        due_datetime=datetime.now() + timedelta(days=1),
                                        is_completed=False,
                                        project=self.project)
        task2 = Task.objects.create(name='Title for the test task 2',
                                    description='Description for the test task',
                                    start_datetime=datetime.now() - timedelta(days=3),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)
        task3 = Task.objects.create(name='Title for the test task 3',
                                    description='Description for the test task',
                                    start_datetime=datetime.now(),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)
        task4 = Task.objects.create(name='Title for the test task 4',
                                    description='Description for the test task',
                                    start_datetime=datetime.now(),
                                    due_datetime=datetime.now() + timedelta(days=1),
                                    is_completed=False,
                                    project=self.project)
        self.tasks = [task1, task2, task3, task4]

    def test_task_automaton_report_week(self):
        report = TaskAutomatonReport(user=self.user, period=7, start_date=datetime.now().date() - timedelta(days=7), end_date=datetime.now().date())
        week_report = report.generate_week_report()
        self.assertIsNotNone(week_report)
        self.assertSetEqual(set(week_report.keys()), {'overall', 'forecast', 'daily', 'trend', 'by_project'})
        self.assertIsInstance(week_report['overall'], dict)
        self.assertSetEqual(set(week_report['overall'].keys()), {'done_ratio', 'late_ratio', 'in_progress_ratio'})

    def test_task_automaton_report_day(self):
        report = TaskAutomatonReport(user=self.user, period=1, start_date=datetime.now().date(), end_date=datetime.now().date())
        day_report = report.generate_day_report()
        self.assertIsNotNone(day_report)
        self.assertSetEqual(set(day_report.keys()), {'overall', 'forecast', 'by_project'})
        self.assertIsInstance(day_report['overall'], dict)
        self.assertSetEqual(set(day_report['overall'].keys()), {'done_ratio', 'late_ratio', 'in_progress_ratio'})