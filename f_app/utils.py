import json
from datetime import datetime

from django_celery_beat.models import PeriodicTask, IntervalSchedule


def new_periodic_task(user_id, url_id, every, *args):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=every,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name='Importing contacts',
        task='f_app.tasks.main',
        args=json.dumps([*args]),
        start_time=datetime.now(),
    )
