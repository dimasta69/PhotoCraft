from django.core.exceptions import ObjectDoesNotExist
from django import forms
from rest_framework import status

from service_objects.fields import ModelField

from utils.services import ServiceWithResult

from functools import lru_cache

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.categories.model import Categories

from typing import Union


class CreatePhotoService(ServiceWithResult):
    title = forms.CharField(required=True)
    description = forms.CharField(required=False)
    current_user = ModelField(User)
    photo = forms.ImageField(required=True)
    category_id = forms.IntegerField(required=False)

    custom_validations = ['category_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._create_photo()
        return self

    def _create_photo(self) -> Photo:
        photo = Photo.objects.create(title=self.cleaned_data['title'],
                                     user=self.cleaned_data.get('current_user'),
                                     category=self.category,
                                     description=self.cleaned_data['description'])
        photo.photo = self.cleaned_data['photo']
        photo.save()
        return photo

    @property
    @lru_cache()
    def category(self) -> Union[Categories, None]:
        try:
            return Categories.objects.get(id=self.cleaned_data['category_id'])
        except Categories.DoesNotExist:
            return None

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

