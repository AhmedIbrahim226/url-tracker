import json

import requests
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import diff_match_patch as dmp_module


def get_url_source_code(url):
    return requests.get(url).text
def custom_0(lis):
    for idx, _ in enumerate(lis):
        if idx == 0 and _[0] == 0:
            yield 0, _[1][-287:]
        elif idx != 0 and _[0] == 0:
            yield 0, _[1][:287]
        else:
            yield _



def check_difference(old_source, new_source):
    dmp = dmp_module.diff_match_patch()
    d = dmp.diff_main(old_source, new_source)
    d = list(custom_0(d))
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
