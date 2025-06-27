from unittest.mock import patch

from django.test import TestCase

from analysis.tasks import make_day_report, make_week_report
from users.models import User


class CeleryTaskTest(TestCase):
    def setUp(self):
        User.objects.create(username='user1', password='XXXX_password')
        User.objects.create(username='user2', password='XXXX_password')
        User.objects.create(username='user3', password='XXXX_password')

    @patch('common.notifications.UserNotificationManger.notify')
    def test_celery_notify_about_day_report(self, mock_notification_manager_class):
        result = make_day_report.delay()
        self.assertTrue(result.successful())
        self.assertTrue(mock_notification_manager_class.called)
        self.assertEqual(mock_notification_manager_class.call_count, 3)

    @patch('common.notifications.UserNotificationManger.notify')
    def test_celery_notify_about_week_report(self, mock_notification_manager_class):
        result = make_week_report.delay()
        self.assertTrue(result.successful())
        self.assertTrue(mock_notification_manager_class.called)
        self.assertEqual(mock_notification_manager_class.call_count, 3)
