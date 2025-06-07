import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScheduleManager.settings')
app = Celery(main='proj', broker="redis://cache:6379/1")
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
app.conf.beat_schedule = {
    'make_week_summary': {
        'task': 'analysis_task.tasks.make_week_summary',
        'schedule': crontab(hour=21, minute=21, day_of_week=1),
    }
    ,
    'make_day_summary': {
        'task': 'analysis.tasks.make_day_summary',
        'schedule': crontab(hour=21, minute=21),
    }

}
