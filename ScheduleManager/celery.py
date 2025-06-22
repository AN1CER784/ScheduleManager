import os
import sys

from celery import Celery
from celery.schedules import crontab

from ScheduleManager import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ScheduleManager.settings')
app = Celery(main='proj')
TESTING = 'test' in sys.argv
TESTING = TESTING or 'test_coverage' in sys.argv or 'unittest' in sys.modules
CELERY = {
    'broker_url': 'redis://redis:6379/1',
    'task_always_eager': TESTING,
    'timezone': settings.TIME_ZONE,
    'result_extended': True,
}
app.config_from_object(CELERY)

app.autodiscover_tasks()
app.conf.beat_schedule = {
    'make_week_summary': {
        'task': 'analysis_task.tasks.make_week_summary',
        'projects': crontab(hour=21, minute=21, day_of_week=1),
    }
    ,
    'make_day_summary': {
        'task': 'analysis.tasks.make_day_summary',
        'projects': crontab(hour=21, minute=21),
    }

}
