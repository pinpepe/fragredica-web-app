# fragredica_web/celery.py
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fragredica_web.settings')
app = Celery('fragredica_web')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
