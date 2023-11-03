from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    # Execute the Speed Test every 10 minutes
    'daily_linkedin_post': {
        'task': 'daily_linkedin_post',
        'schedule': crontab(minute='*/30'),
    },
    'weekly_database_export': {
        'task': 'weekly_database_export',
        'schedule': crontab(minute='*/1'), #crontab(minute=0, hour=0, day_of_month='*/3')
    },
}