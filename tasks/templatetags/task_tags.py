from django import template

register = template.Library()

@register.simple_tag()
def group_comments_by_date(comments):
    grouped_comments = {}
    for comment in comments:
        date = comment.created_date
        if date not in grouped_comments:
            grouped_comments[date] = []
        grouped_comments[date].append(comment)
    return grouped_comments
