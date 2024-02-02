# from celery import shared_task
# from models_app.models.photo.model import Photo
#
#
# @shared_task()
# def my_task():
#     Photo.objects.filter(status='Delete').delete()
#     return "12312312"

from photo_craft.celery import app
from models_app.models.photo.model import Photo
from utils.fd import dela


@app.task
def my_task():
    dela()
    return None
