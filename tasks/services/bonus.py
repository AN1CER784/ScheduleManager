from django.conf import settings
from django.db import transaction
from django.db.models import F

from users.models import BonusTransaction, User


def apply_bonus(user: User, task, points: int, reason: str) -> BonusTransaction | None:
    if points == 0:
        return None
    with transaction.atomic():
        BonusTransaction.objects.create(user=user, task=task, points=points, reason=reason)
        User.objects.filter(pk=user.pk).update(bonus_balance=F('bonus_balance') + points)
    return BonusTransaction.objects.filter(user=user, task=task, points=points, reason=reason).latest("created_at")


def get_bonus_points_on_time() -> int:
    return getattr(settings, "BONUS_POINTS_ON_TIME", 10)


def get_bonus_points_overdue_penalty() -> int:
    return getattr(settings, "BONUS_POINTS_OVERDUE_PENALTY", -5)
