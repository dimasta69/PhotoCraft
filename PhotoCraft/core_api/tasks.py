import os

from django.utils.timezone import make_aware

from photo_craft.celery import app
from models_app.models.photo.model import Photo
from datetime import datetime
from photo_craft.settings.celery import OBJECT_TIME_DELETE


@app.task
def my_task():
    for photo in Photo.objects.all():
        if photo.status == "Delete" and photo.deleted_at + OBJECT_TIME_DELETE <= make_aware(datetime.now()):
            if os.path.isfile(photo.photo.path):
                os.remove(photo.photo.path)
            if photo.backup_photo:
                if os.path.isfile(photo.backup_photo.path):
                    os.remove(photo.backup_photo.path)
            photo.delete()
