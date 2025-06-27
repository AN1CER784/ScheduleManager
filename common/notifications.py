from django.core.mail import send_mail


class UserNotificationManger:
    def __init__(self, user, builder, fetcher=None):
        self.user = user
        self.builder = builder
        self.fetcher = fetcher

    def notify(self):
        if self.fetcher:
            objects = self.fetcher.fetch(self.user)
            mail_dict = self.builder.build(self.user, objects)
        else:
            mail_dict = self.builder.build(self.user)
        subject, message, recipient_list, html_message = mail_dict
        send_mail(subject=subject, message=message, from_email=None, recipient_list=recipient_list, fail_silently=False, html_message=html_message)