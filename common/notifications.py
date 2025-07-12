from typing import Protocol

from django.core.mail import send_mail
from django.db.models import QuerySet

from users.models import User


class BuilderProtocol(Protocol):
    @classmethod
    def build(cls, user: User, objects: QuerySet | None = None) -> tuple[str, str, list[str], str]:
        ...


class FetcherProtocol(Protocol):
    @classmethod
    def fetch(cls, user: User) -> QuerySet | None:
        ...


class UserNotificationManager:
    def __init__(self, user: User, builder: type(BuilderProtocol), fetcher: type(FetcherProtocol) | None = None):
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
        send_mail(subject=subject, message=message, from_email=None, recipient_list=recipient_list, fail_silently=False,
                  html_message=html_message)
