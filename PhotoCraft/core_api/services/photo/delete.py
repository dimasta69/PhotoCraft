from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.categories.model import Categories

from functools import lru_cache

from utils.services import ServiceWithResult

from service_objects.fields import ModelField


class PhotoDeleteService(ServiceWithResult):
    id = forms.IntegerField(required=True)
    current_user = ModelField(User)

    custom_validations = ['photo_presence', 'user_ratio']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete()
        return self

    def _delete(self):
        photo = self.get_photo
        photo.delete()
        return Photo.objects.none()

    @property
    @lru_cache()
    def get_photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['id'])
        except Photo.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['id']:
            if not self.get_photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))

    def user_ratio(self):
        if not ((self.get_photo.user_id.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
