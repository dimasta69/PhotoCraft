CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
BROKER_CONNECTION_RETRY_ON_STARTUP = True

# CELERY_BEAT_SCHEDULE = {
#     'delete-objects': {
#         'task': 'core_api.tasks.my_task',
#         'schedule': 60,  # 300 секунд = 5 минут
#     },
# }

