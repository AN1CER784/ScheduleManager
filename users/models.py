from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'user'
