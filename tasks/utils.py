from django_celery_beat.models import PeriodicTask


def delete_periodic_task(name):
    PeriodicTask.objects.filter(name=name).delete()

