from django.contrib.auth.forms import PasswordResetForm
from celery import shared_task

from users.models import User


@shared_task
def task_send_mail(subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name, user_id):
    context['user'] = User.objects.get(pk=user_id)
    PasswordResetForm().send_mail(subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name)