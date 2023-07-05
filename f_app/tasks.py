from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from time import sleep



@shared_task(bind=True)
def my_task(self, p1, p2):
    try:
        for x in range(500):
            print(x)
            sleep(1)
    except SoftTimeLimitExceeded as time_limit:
        pass

@shared_task(bind=True)
def main(self, *args):
    my_task.apply_async(args, soft_time_limit=10)
