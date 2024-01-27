from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist

from service_objects.fields import ModelField

from models_app.models.liked.model import Liked
from models_app.models.photo.model import Photo
from models_app.models.users.model import User

from utils.services import ServiceWithResult


class LikedService(ServiceWithResult):
    photo_id = forms.IntegerField(required=True)
    current_user = ModelField(User)

    custom_validations = ['photo_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._check_data()
        return self

    def _check_data(self):
        if not self.get_liked:
            like = Liked.objects.create(photo_id=self.get_photo, user_id=self.cleaned_data['current_user'])
            print(1234)
            print(like.photo_id)
            like.save()
            return like
        self.get_liked.delete()

    @property
    @lru_cache()
    def get_photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def get_liked(self):
        try:
            return Liked.objects.get(photo_id=self.get_photo, user_id=self.cleaned_data['current_user'])
        except Liked.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['photo_id']:
            if not self.get_photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))
