from django.test import TransactionTestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model
from users.notifications import UserSignUpNotificationBuilder
from users.tasks import reset_password_task_send_mail

User = get_user_model()

class UserSignUpNotificationTestCase(TransactionTestCase):
    @patch('users.signals.notify_user_about_sign_up.delay')
    def test_user_signup_notification(self, mock_delay):
        User.objects.create_user(username='testuser', email='test@example.com', password='123456')
        self.assertTrue(mock_delay.called)

    def test_user_signup_notification_builder(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='123456')
        builder = UserSignUpNotificationBuilder()
        subject, message, recipient_list, html_message = builder.build(user)
        self.assertEqual(subject, 'Welcome to ScheduleManager')
        self.assertEqual(recipient_list, ['test@example.com'])
        self.assertIn("Welcome to our platform! We're excited to have you on board.", message)

class UserResetPasswordNotificationTestCase(TransactionTestCase):
    @patch('users.tasks.PasswordResetForm.send_mail')
    def test_user_reset_password_notification(self, mock_notify):
        user = User.objects.create_user(username='XXXXXXXX', email='test@example.com', password='123456')
        result = reset_password_task_send_mail.delay(
            subject_template_name='registration/password_reset_subject.txt',
            email_template_name='registration/password_reset_email.html',
            context={},
            from_email='noreply@example.com',
            to_email='test@example.com',
            html_email_template_name=None,
            user_id=user.id
        )
        self.assertTrue(result.successful())
        self.assertTrue(mock_notify.called)