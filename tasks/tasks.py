from celery import shared_task
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from tasks.models import Task
from tasks.services.bonus import apply_bonus, get_bonus_points_overdue_penalty


@shared_task
def apply_overdue_penalties() -> int:
    now = timezone.now()
    overdue_tasks = (Task.objects
                     .select_related("assignee")
                     .filter(deadline__isnull=False,
                             deadline__lt=now,
                             overdue_penalty_applied=False)
                     .exclude(status=Task.Status.DONE))
    count = 0
    for task in overdue_tasks:
        apply_bonus(task.assignee, task, get_bonus_points_overdue_penalty(), _("Overdue task penalty"))
        task.overdue_penalty_applied = True
        task.save(update_fields=["overdue_penalty_applied"])
        count += 1
    return count
