from service_objects.services import Service

from django import forms

from models_app.models.liked.model import Liked
from models_app.models.photo.model import Photo
from models_app.models.users.model import Users


class LikedService(Service):
    photo_id = forms.IntegerField(required=True)
    users_id = forms.IntegerField(required=True)

    def process(self):
        if self.is_valid():
            return self._check_data
        return self

    @property
    def _check_data(self):
        photo = Photo.objects.get(id=self.cleaned_data['photo_id']).id
        user = Users.objects.get(id=self.cleaned_data['user_id']).id
        if Liked.objects.get(photo_id=photo, user_id=user):
            Liked.objects.get(photo_id=photo, user_id=user).delete()
            return Liked.objects.none()
        return Liked.objects.create(photo_id=photo, user_id=user)
