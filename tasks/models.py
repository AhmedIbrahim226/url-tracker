from django.db import models
from core.celery import app


class TaskControl(models.Model):
    url_model = models.ForeignKey(to='tracker.UrlModel', on_delete=models.CASCADE, null=True, blank=True, related_name='url_model_task_control')
    uuid = models.CharField(max_length=100)

    def __str__(self):
        return self.uuid

    @property
    def revoke_celery_task(self):
        app.control.revoke(self.uuid, terminate=True, signal='SIGKILL')
        return
