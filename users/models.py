from django.contrib.auth.models import AbstractUser
from django.db import models

from ScheduleManager import settings


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    language = models.CharField(max_length=10, default='en-us', choices=settings.LANGUAGES)

    class Meta:
        db_table = 'user'
