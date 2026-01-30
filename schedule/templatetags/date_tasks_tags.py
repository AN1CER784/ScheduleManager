from collections import defaultdict
from datetime import timedelta, datetime
from typing import Literal, TypedDict, NamedTuple

from django import template
from django.db.models import Q

from tasks.models import Task

register = template.Library()


class TaskWithType(TypedDict):
    task: Task
    type: Literal["created_at", "deadline"]


@register.simple_tag(takes_context=True)
def get_tasks_by_date(context, calendar_start_date: datetime.date, calendar_end_date: datetime.date) \
        -> dict[datetime.date, list[TaskWithType]]:
    tasks = context['tasks'].filter(
        Q(created_at__date__range=[calendar_start_date, calendar_end_date]) | Q(
            deadline__date__range=[calendar_start_date, calendar_end_date])
    )
    tasks_by_date = defaultdict(list)
    for task in tasks:
        tasks_by_date[task.created_at.date()].append(TaskWithType(task=task, type="created_at"))
        if task.deadline:
            tasks_by_date[task.deadline.date()].append(TaskWithType(task=task, type="deadline"))
    return tasks_by_date


@register.filter
def get_day_type(tasks_list: list[TaskWithType]) -> bool:
    return any(value == "deadline" for task in tasks_list for key, value in task.items())


class MonthDates(NamedTuple):
    start_of_month: datetime.date
    end_of_month: datetime.date


@register.simple_tag
def get_dates_of_month(month_date: datetime.date) -> MonthDates:
    start_of_month = month_date.replace(day=1)
    next_month = start_of_month.replace(month=start_of_month.month + 1,
                                        day=1) if start_of_month.month < 12 else start_of_month.replace(
        year=start_of_month.year + 1, month=1, day=1)
    end_of_month = next_month - timedelta(days=1)
    return MonthDates(start_of_month=start_of_month, end_of_month=end_of_month)
