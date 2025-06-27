from django.template.loader import render_to_string


class UserSignUpNotificationBuilder:
    @staticmethod
    def build(user):
        subject = 'Welcome to ScheduleManager'
        recipient_list = [user.email]
        message = render_to_string('users/emails/user_register_email_text.html', context={'user': user})
        html_message = render_to_string('users/emails/user_register_email.html', context={'user': user})
        return subject, message, recipient_list, html_message