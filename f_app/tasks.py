import requests
from celery import shared_task

from .models import UrlModel, ChangesStore
from .utils import check_difference




@shared_task(bind=True)
def monitor_url_changes(self, url_model_id):
    url_model = UrlModel.objects.get(id=url_model_id)
    user =  url_model.user
    url = url_model.url
    old_source = url_model.source_code
    new_source = requests.get(url=url).text

    result = check_difference(old_source=old_source, new_source=new_source)

    # send_mail(
    #     'Diffrence in your link. ' + '(' + scraper.url + ')',
    #     'THE OLD: ' + check + '\nTHE NEW: ' + source,
    #     settings.EMAIL_HOST_USER,
    #     [scraper.user.email],
    # )

    ChangesStore.objects.create(user=user, url_model=url_model, description=result)
    url_model.source_code = new_source
    url_model.save()


@shared_task(bind=True)
def config_periodic_task_child_tasks(self):
    pass
