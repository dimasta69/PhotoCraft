from photo_craft.celery import app
from models_app.models.photo.model import Photo
from datetime import datetime
from photo_craft.settings.celery import OBJECT_TIME_DELETE


@app.task
def my_task():
    for photo in Photo.objects.all():
        if photo.status == "Delete" and photo.deleted_at + OBJECT_TIME_DELETE <= datetime.now():
            photo.delete()
