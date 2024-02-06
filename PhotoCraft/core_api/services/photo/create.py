from django.core.exceptions import ObjectDoesNotExist
from django import forms

from service_objects.fields import ModelField

from utils.services import ServiceWithResult

from functools import lru_cache

from models_app.models.photo.model import Photo
from models_app.models.users.model import User
from models_app.models.categories.model import Categories


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
            self.result = self._create_obj()
        return self

    def _create_obj(self):
        photo = Photo.objects.create(title=self.cleaned_data['title'],
                                     user_id=self.cleaned_data.get('current_user'),
                                     category_id=self.category,
                                     description=self.cleaned_data['description'])
        photo.photo = self.cleaned_data['photo']
        photo.save()
        return photo

    @property
    @lru_cache()
    def category(self):
        try:
            return Categories.objects.get(id=self.cleaned_data['category_id'])
        except Categories.DoesNotExist:
            return None

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))
