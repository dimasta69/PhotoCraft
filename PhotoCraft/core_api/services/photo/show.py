from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models.photo.model import Photo
from models_app.models.users.model import User

from utils.services import ServiceWithResult

from functools import lru_cache

from service_objects.fields import ModelField


class PhotoService(ServiceWithResult):
    id = forms.IntegerField(required=True)
    current_user = forms.IntegerField(required=False)

    custom_validations = ['photo_presence', 'current_user_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._show()
        return self

    def _show(self):
        if self.cleaned_data['current_user']:
            if self.user.is_superuser or self.user == self.photo.user_id:
                return self.photo
            self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                          f"{self.cleaned_data['id']} i don't have access rights to "
                                                          f"this post"))
        if self.photo.status == 'Published':
            return self.photo
        self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                      f"{self.cleaned_data['id']} not found"))

    @property
    @lru_cache()
    def photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def user(self):
        try:
            return User.objects.get(id=self.cleaned_data['current_user'])
        except User.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['id']:
            if not self.photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))

    def current_user_presence(self):
        if self.cleaned_data.get('current_user'):
            if not self.user:
                self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                                  f"{self.cleaned_data['current_user']} not found"))
