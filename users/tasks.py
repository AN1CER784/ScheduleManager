from celery import shared_task
from django.contrib.auth.forms import PasswordResetForm
from django.utils import translation

from common.notifications import UserNotificationManger
from users.models import User
from users.notifications import UserSignUpNotificationBuilder


@shared_task
def reset_password_task_send_mail(subject_template_name, email_template_name, context, from_email, to_email,
                                  html_email_template_name, user_id):
    context['user'] = User.objects.get(pk=user_id)
    with translation.override(context['user'].language):
        PasswordResetForm().send_mail(subject_template_name,
                                      email_template_name,
                                      context,
                                      from_email,
                                      to_email,
                                      html_email_template_name)


@shared_task
def notify_user_about_sign_up(user_id):
    user = User.objects.get(pk=user_id)
    user_notification_manager = UserNotificationManger(user=user, builder=UserSignUpNotificationBuilder)
    user_notification_manager.notify()
