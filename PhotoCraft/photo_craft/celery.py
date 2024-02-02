from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'photo_craft.settings')
app = Celery('photo_craft')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'every': {
#         'task': 'core_api.tasks.my_task',
#         'schedule': crontab(),  # по умолчанию выполняет каждую минуту, очень гибко
#     },  # настраивается
#
# }

