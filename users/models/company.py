from django.db import models

from common.models import AbstractCreatedModel


class Company(AbstractCreatedModel):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        verbose_name = "company"
        ordering = ["name"]

    def __str__(self):
        return self.name