from datetime import datetime, timedelta

from django.test import TestCase
from django.urls import reverse

from projects.models import Project


class ScheduleCalendarViewTestCase(TestCase):
    def test_schedule_calendar_view(self):
        response = self.client.get(reverse('schedule:calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedule/calendar.html")

    def test_schedule_calendar_with_tasks(self):
        project = Project.objects.create(name="Test Project")
        task1 = project.tasks.create(name='Test Task 1',
                                      description='Description for the test task',
                                      start_datetime=datetime.now(),
                                      due_datetime=datetime.now() + timedelta(days=1),
                                      is_completed=False,
                                      project=project)

        task2 = project.tasks.create(name='Test Task 2',
                                      description='Description for the test task',
                                      start_datetime=datetime.now(),
                                      due_datetime=datetime.now() + timedelta(days=1),
                                      is_completed=False,
                                      project=project)
        response = self.client.get(reverse('schedule:calendar'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "schedule/calendar.html")


