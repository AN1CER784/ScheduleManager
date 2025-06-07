from celery import shared_task


@shared_task
def make_day_summary():
    from .management.commands.make_day_summary import Command
    Command().handle()


@shared_task
def make_week_summary():
    from .management.commands.make_week_summary import Command
    Command().handle()
