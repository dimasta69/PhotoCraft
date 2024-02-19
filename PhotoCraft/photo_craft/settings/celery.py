import os
from dotenv import load_dotenv
import datetime

load_dotenv()

CELERY_BROKER_URL = os.getenv('BROKER_URL')
CELERY_RESULT_BACKEND = os.getenv('RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = [os.getenv('ACCEPT_CONTENT')]
CELERY_TIMEZONE = os.getenv('TIMEZONE')
CELERY_TASK_SERIALIZER = os.getenv('TASK_SERIALIZER')
CELERY_RESULT_SERIALIZER = os.getenv('RESULT_SERIALIZER')
OBJECT_TIME_DELETE = datetime.timedelta(minutes=int(os.getenv('OBJECT_TIME_DELETE')))
#CELERY_TASK_ALWAYS_EAGER = True

CELERY_BEAT_SCHEDULE = {
    'delete-objects': {
        'task': 'core_api.tasks.my_task',
        'schedule': OBJECT_TIME_DELETE,
    },
}
