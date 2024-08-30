from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_management_api.settings')
app = Celery('hospital_management_api', broker="pyamqp://admin:admin@hma_rabbitmq//",
             )
app.config_from_object('django.conf:settings', namespace='CELERY')


app.conf.beat_schedule = {
    'generate-slots-every-monday': {
        'task': 'appointments.tasks.periodic_tst',
        'schedule': crontab(day_of_week=1, hour=0, minute=0),
    },
}


app.autodiscover_tasks()
