from django.template.loader import render_to_string
from django.utils import translation
from django.utils.translation import gettext_lazy as _


class UserSignUpNotificationBuilder:
    @staticmethod
    def build(user):
        with translation.override(user.language):
            subject = _('Welcome to ScheduleManager')
            recipient_list = [user.email]
            message = render_to_string('users/emails/user_register_email_text.html', context={'user': user})
            html_message = render_to_string('users/emails/user_register_email.html', context={'user': user})
            return subject, message, recipient_list, html_message
