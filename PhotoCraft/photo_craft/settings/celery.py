CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
DATE_TIME_DELETE = 120

CELERY_BEAT_SCHEDULE = {
    'delete-objects': {
        'task': 'core_api.tasks.my_task',
        'schedule': DATE_TIME_DELETE,
    },
}
