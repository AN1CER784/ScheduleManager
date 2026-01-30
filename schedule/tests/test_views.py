from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from projects.models import Project
from tasks.models import Task
from users.models import User, Company


class ScheduleCalendarViewTestCase(TestCase):
    def setUp(self):
        self.company = Company.objects.create(name="Acme")
        self.user = User.objects.create_user(username='user', password='pass', company=self.company)
        self.client.login(username='user', password='pass')

    def test_schedule_calendar_view(self):
        response = self.client.get(reverse('schedule:calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedule/schedule.html")

    def test_schedule_calendar_with_tasks(self):
        project = Project.objects.create(name="Test Project", company=self.company, created_by=self.user)
        Task.objects.create(name='Test Task 1',
                            project=project,
                            creator=self.user,
                            assignee=self.user,
                            deadline=timezone.now() + timedelta(days=1))

        Task.objects.create(name='Test Task 2',
                            project=project,
                            creator=self.user,
                            assignee=self.user,
                            deadline=timezone.now() + timedelta(days=2))
        response = self.client.get(reverse('schedule:calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedule/schedule.html")

    def test_schedule_filters_by_project(self):
        project_a = Project.objects.create(name="Project A", company=self.company, created_by=self.user)
        project_b = Project.objects.create(name="Project B", company=self.company, created_by=self.user)
        Task.objects.create(name='Task A',
                            project=project_a,
                            creator=self.user,
                            assignee=self.user,
                            deadline=timezone.now() + timedelta(days=1))
        Task.objects.create(name='Task B',
                            project=project_b,
                            creator=self.user,
                            assignee=self.user,
                            deadline=timezone.now() + timedelta(days=1))
        response = self.client.get(reverse('schedule:calendar'), {'project': project_a.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Task A')
        self.assertNotContains(response, 'Task B')
