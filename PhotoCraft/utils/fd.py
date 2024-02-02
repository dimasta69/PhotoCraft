from models_app.models.photo.model import Photo


def dela():
    photo = Photo.objects.get(id=1)
    photo.delete()
    print(223412414)
