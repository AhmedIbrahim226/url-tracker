import json

import requests
from django.utils import timezone
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import diff_match_patch as dmp_module


def get_url_source_code(url):
    return requests.get(url).text
def define_0(value):
    f = [list(x) for x in value]
    start = None
    end = None
    if f[0][0] == 0:
        start = f[0][1][-150:]
    if f[-1][0] == 0:
        end = f[-1][1][:150]

    f[0][1] = start
    f[-1][1] = end
    return f



def check_difference(old_source, new_source):
    dmp = dmp_module.diff_match_patch()
    d = dmp.diff_main(old_source, new_source)
    d = define_0(d)
    dmp.diff_cleanupSemantic(d)
    result = dmp.diff_prettyHtml(d)
    return result

def new_periodic_task(user_id, url_model_id, every):
    schedule, created = IntervalSchedule.objects.get_or_create(
        every=every,
        period=IntervalSchedule.MINUTES,
    )
    PeriodicTask.objects.create(
        interval=schedule,
        name=f'user_{user_id}_url_{url_model_id}',
        task='f_app.tasks.monitor_url_changes',
        args=json.dumps([url_model_id])
    )
