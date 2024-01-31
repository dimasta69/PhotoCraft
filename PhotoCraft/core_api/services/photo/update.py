from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.categories.model import Categories

from functools import lru_cache

from utils.services import ServiceWithResult

from service_objects.fields import ModelField


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
        return self

    def _update_photo(self):
        photo = self.get_photo
        photo.title = self.cleaned_data['title']
        photo.description = self.cleaned_data['description']
        photo.category_id = self.get_category
        if self.cleaned_data['photo']:
            photo.backup_photo = photo.photo
            photo.photo = self.cleaned_data['photo']
        photo.update()
        photo.save()
        return photo

    @property
    @lru_cache()
    def get_photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['id'])
        except Photo.DoesNotExist:
            return None

    @property
    @lru_cache()
    def get_category(self):
        try:
            return Categories.objects.get(id=self.cleaned_data['category_id'])
        except Categories.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['id']:
            if not self.get_photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.get_category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))

    def user_ratio(self):
        if not ((self.get_photo.user_id.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))


