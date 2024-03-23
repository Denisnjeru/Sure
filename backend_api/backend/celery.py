from __future__ import absolute_import, unicode_literals

import os
import sys

from celery import Celery

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.development')

from django.conf import settings

app = Celery('backend', backeqnd=settings.CELERY_RESULT_BACKEND, broker=settings.CELERY_BROKER_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.loader.override_backends['django-db'] = 'django_celery_results.backends.database:DatabaseBackend'


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')