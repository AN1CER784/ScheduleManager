from datetime import timedelta

from django import template
from django.db.models import Q
from collections import defaultdict

register = template.Library()


@register.simple_tag(takes_context=True)
def get_tasks_by_date(context, calendar_start_date, calendar_end_date):
    tasks = context['tasks'].filter(
        Q(start_datetime__date__range=[calendar_start_date, calendar_end_date]) | Q(due_datetime__date__range=[calendar_start_date, calendar_end_date])
    )
    tasks_by_date = defaultdict(list)
    for task in tasks:
        tasks_by_date[task.start_datetime.date()].append({task: "start_datetime"})
        if task.due_datetime:
            tasks_by_date[task.due_datetime.date()].append({task: "due_datetime"})
    return tasks_by_date

@register.filter
def get_day_type(tasks_list):
    return any(value == "due_datetime" for task in tasks_list for key, value in task.items())

@register.simple_tag
def get_dates_of_month(month_date):
    start_of_month = month_date.replace(day=1)
    next_month = start_of_month.replace(month=start_of_month.month + 1,
                                        day=1) if start_of_month.month < 12 else start_of_month.replace(
        year=start_of_month.year + 1, month=1, day=1)
    end_of_month = next_month - timedelta(days=1)
    return {
        "start_of_month": start_of_month,
        "end_of_month": end_of_month
    }

