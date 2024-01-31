from celery import shared_task
from models_app.models.photo.model import Photo


@shared_task
def delete_photo(photo_id):
    photo = Photo.objects.get(id=photo_id)
    photo.delete()


@shared_task
def schedule_photo_deletion(photo_id):
    delete_photo.apply_async(args=(photo_id,), countdown=180)
