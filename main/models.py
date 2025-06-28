from django.db import models


class Page(models.Model):
    key = models.CharField(max_length=40, primary_key=True)
    content = models.TextField()
