from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.tasks import notify_user_about_sign_up

User = get_user_model()


@receiver(post_save, sender=User)
def post_sign_up_signal(sender, instance, created, **kwargs):
    if created:
        transaction.on_commit(lambda: notify_user_about_sign_up.delay(instance.id))
