import requests
from bs4 import BeautifulSoup
from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded
from time import sleep

from .models import UrlModel
from .utils import check_difference




@shared_task(bind=True)
def monitor_url_changes(self, url_model_id):
    url_model = UrlModel.objects.get(id=url_model_id)
    check_difference(old_source='', new_source='')
    for i in range(65):
        print(i)
        sleep(1)
    # list_scrap = []
    # for name in UrlModel.objects.all():
    #     soup = BeautifulSoup(requests.get(name.url).text, 'html.parser')
    #     for scraping in soup.prettify().split('\n'):
    #         list_scrap.append(scraping.strip())
    #     UrlModel.objects.filter(url=name.url).update(
    #         source_code='\n'.join(list_scrap)
    #     )
    #     list_scrap.clear()

@shared_task(bind=True)
def config_periodic_task_child_tasks(self):
    pass
