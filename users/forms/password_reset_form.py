from django.contrib.auth.forms import PasswordResetForm as PasswordResetFormCore

from users.tasks import reset_password_task_send_mail


class PasswordResetForm(PasswordResetFormCore):
    def send_mail(
            self,
            subject_template_name,
            email_template_name,
            context,
            from_email,
            to_email,
            html_email_template_name=None,
    ):
        user_id = context['user'].id
        context.pop('user')
        reset_password_task_send_mail.delay(subject_template_name, email_template_name, context, from_email, to_email,
                                            html_email_template_name, user_id)
