from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from models_app.models.categories.model import Categories
from models_app.models.users.model import User

from service_objects.fields import ModelField

from functools import lru_cache

from utils.services import ServiceWithResult


class CategoryDeleteServcie(ServiceWithResult):
    id = forms.IntegerField(required=True)
    current_user = ModelField(User)

    custom_validations = ['category_presence', 'user_ratio']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_category()
        return self

    def _delete_category(self):
        self.category.delete()
        return Categories.objects.none()

    @property
    @lru_cache()
    def category(self):
        try:
            return Categories.objects.get(id=self.cleaned_data['id'])
        except Categories.DoesNotExist:
            return None

    def category_presence(self):
        if self.cleaned_data['id']:
            if not self.category:
                self.add_error('id', ObjectDoesNotExist(f"Category with id="
                                                        f"{self.cleaned_data['category_id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def user_ratio(self):
        if not self.cleaned_data['current_user'].is_superuser:
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
            self.response_status = status.HTTP_403_FORBIDDEN
