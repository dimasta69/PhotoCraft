from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.categories.model import Categories

from functools import lru_cache

from utils.services import ServiceWithResult

from service_objects.fields import ModelField

from typing import Union, List


class UpdatePhotoService(ServiceWithResult):
    id = forms.IntegerField(required=True)
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    current_user = ModelField(User)
    photo = forms.ImageField(required=False)
    category_id = forms.IntegerField(required=False)

    custom_validations = ['category_presence', 'photo_presence', 'user_ratio']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_photo()
            self.response_status = status.HTTP_201_CREATED
        return self

    def _update_photo(self) -> Photo:
        if self.cleaned_data['title']:
            self.photo_obj.title = self.cleaned_data['title']
        if self.cleaned_data['description']:
            self.photo_obj.description = self.cleaned_data['description']
        if self.cleaned_data['category_id']:
            self.photo_obj.category = self.category
        if self.cleaned_data['photo']:
            self.photo_obj.backup_photo = self.photo_obj.photo
            self.photo_obj.photo = self.cleaned_data['photo']
        self.photo_obj.set_update()
        return self.photo_obj

    @property
    @lru_cache()
    def photo_obj(self) -> Union[Photo, None]:
        try:
            return Photo.objects.get(id=self.cleaned_data['id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def category(self) -> Union[Categories, None]:
        try:
            return Categories.objects.get(id=self.cleaned_data['category_id'])
        except Categories.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['id']:
            if not self.photo_obj:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def user_ratio(self):
        if not ((self.photo_obj.user.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error(
                "current_user",
                f"Material with id = {self.cleaned_data['current_user']} does not found",
            )
            self.response_status = status.HTTP_403_FORBIDDEN


