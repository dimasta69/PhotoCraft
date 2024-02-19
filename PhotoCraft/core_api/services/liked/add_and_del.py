from functools import lru_cache

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

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
        if not self.liked:
            like = Liked.objects.create(photo_id=self.photo, user_id=self.cleaned_data['current_user'])
            like.save()
            return like
        self.liked.delete()

    @property
    @lru_cache()
    def photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['photo_id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def liked(self):
        try:
            return Liked.objects.get(photo_id=self.photo, user_id=self.cleaned_data['current_user'])
        except Liked.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['photo_id']:
            if not self.photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND
