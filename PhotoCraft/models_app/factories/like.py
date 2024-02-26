import factory
from factory.django import DjangoModelFactory

from models_app.models.liked.model import Liked
from models_app.models.photo.model import Photo
from models_app.models.users.model import User


class LikeFactory(DjangoModelFactory):
    class Meta:
        model = Liked

    photo_id = factory.Iterator(Photo.objects.all().values_list('id', flat=True))
    user_id = factory.Iterator(User.objects.all().values_list('id', flat=True))
