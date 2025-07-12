import logging

from celery import shared_task
from django.contrib.auth.forms import PasswordResetForm
from django.utils import translation

from common.notifications import UserNotificationManager
from users.models import User
from users.notifications import UserSignUpNotificationBuilder

logger = logging.getLogger(__name__)


@shared_task
def reset_password_task_send_mail(subject_template_name: str, email_template_name: str, context: dict, from_email: str, to_email: str,
                                  html_email_template_name: str, user_id: int) -> None:
    context['user'] = User.objects.get(pk=user_id)
    with translation.override(context['user'].language):
        PasswordResetForm().send_mail(subject_template_name,
                                      email_template_name,
                                      context,
                                      from_email,
                                      to_email,
                                      html_email_template_name)


@shared_task
def notify_user_about_sign_up(user_id: int) -> None:
    user = User.objects.get(pk=user_id)
    user_notification_manager = UserNotificationManager(user=user, builder=UserSignUpNotificationBuilder) # noqa
    with translation.override(user.language):
        try:
            user_notification_manager.notify()
        except Exception as e:
            logger.exception(f"Failed to notify user about registration {user.id} - {user.email}: {e}")
