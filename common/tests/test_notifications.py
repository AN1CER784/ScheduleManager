from unittest.mock import Mock

from django.test import TestCase

from common.notifications import UserNotificationManger
from django.core import mail

class UserNotificationMangerTestCase(TestCase):
    def test_notify_with_fetcher(self):
        mock_fetcher = Mock()
        mock_builder = Mock()
        mock_user = Mock()
        mock_fetcher.fetch.return_value = ['object1', 'object2']
        mock_builder.build.return_value = (
            'Test Subject',
            'Test Message',
            ['user@example.com'],
            '<p>Test HTML</p>'
        )

        manager = UserNotificationManger(user=mock_user, builder=mock_builder, fetcher=mock_fetcher)


        mail.outbox = []

        manager.notify()

        mock_fetcher.fetch.assert_called_once_with(mock_user)
        mock_builder.build.assert_called_once_with(['object1', 'object2'], mock_user)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject')
        self.assertEqual(mail.outbox[0].to, ['user@example.com'])
        self.assertEqual(mail.outbox[0].message(), 'Test Message')
        self.assertEqual(mail.outbox[0].alternatives[0][0], '<p>Test HTML</p>')

    def test_notify_without_fetcher(self):
        mock_builder = Mock()
        mock_user = Mock()

        mock_builder.build.return_value = (
            'Test Subject No Fetcher',
            'Test Message No Fetcher',
            ['user2@example.com'],
            '<p>Test No Fetcher HTML</p>'
        )

        manager = UserNotificationManger(user=mock_user, builder=mock_builder)

        from django.core import mail
        mail.outbox = []

        manager.notify()

        mock_builder.build.assert_called_once_with(mock_user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test Subject No Fetcher')
        self.assertEqual(mail.outbox[0].to, ['user2@example.com'])
        self.assertEqual(mail.outbox[0].message(), 'Test Message No Fetcher')
        self.assertEqual(mail.outbox[0].alternatives[0][0], '<p>Test No Fetcher HTML</p>')