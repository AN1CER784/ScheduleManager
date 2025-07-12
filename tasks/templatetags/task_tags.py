from collections import defaultdict
from datetime import datetime

from django import template
from django.db.models import QuerySet

from tasks.models import TaskComment

register = template.Library()


@register.simple_tag()
def group_comments_by_date(comments: QuerySet[TaskComment]) -> dict[datetime.date, list[TaskComment]]:
    grouped_comments = defaultdict(list)
    for comment in comments:
        date = comment.created_date
        grouped_comments[date].append(comment)
    return grouped_comments
