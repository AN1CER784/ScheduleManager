from __future__ import annotations

from datetime import timedelta

from django.db.models import Q, QuerySet
from django.utils import timezone

from tasks.models import Task


def apply_task_filters(queryset: QuerySet[Task], params) -> QuerySet[Task]:
    assignee = params.get("assignee")
    if assignee:
        queryset = queryset.filter(assignee_id=assignee)

    creator = params.get("creator")
    if creator:
        queryset = queryset.filter(creator_id=creator)

    priority = params.get("priority")
    if priority:
        queryset = queryset.filter(priority=priority)

    statuses = params.getlist("status") if hasattr(params, "getlist") else []
    if not statuses:
        raw_statuses = params.get("status")
        statuses = [s for s in raw_statuses.split(",") if s] if raw_statuses else []
    if statuses:
        queryset = queryset.filter(status__in=statuses)

    deadline_filter = params.get("deadline")
    if deadline_filter == "none":
        queryset = queryset.filter(deadline__isnull=True)
    elif deadline_filter == "overdue":
        queryset = queryset.filter(deadline__lt=timezone.now()).exclude(status=Task.Status.DONE)
    elif deadline_filter == "today":
        queryset = queryset.filter(deadline__date=timezone.localdate())
    elif deadline_filter == "next3":
        end_date = timezone.now() + timedelta(days=3)
        queryset = queryset.filter(deadline__date__range=[timezone.localdate(), end_date.date()])
    elif deadline_filter == "next7":
        end_date = timezone.now() + timedelta(days=7)
        queryset = queryset.filter(deadline__date__range=[timezone.localdate(), end_date.date()])

    q = params.get("q")
    if q:
        queryset = queryset.filter(Q(name__icontains=q) | Q(description__icontains=q))

    return queryset
