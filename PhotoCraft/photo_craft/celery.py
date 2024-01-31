import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_craft.settings')

app = Celery('photo_craft')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

