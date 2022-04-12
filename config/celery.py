from __future__ import absolute_import

import os

import django
from celery import Celery, shared_task
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ.setdefault("FORKED_BY_MULTIPROCESSING", "1")
app = Celery("config", broker=settings.BROKER_URL)
django.setup()

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@shared_task
def tester():
    print('hellow')


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
