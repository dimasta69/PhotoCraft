from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from django import forms
from rest_framework import status

from service_objects.fields import ModelField

from utils.services import ServiceWithResult

from models_app.models.users.model import User
from models_app.models.categories.model import Categories

from typing import Union, List


class CategoryUpdateServcie(ServiceWithResult):
    id = forms.IntegerField(required=True)
    title = forms.CharField(required=True)
    current_user = ModelField(User)

    custom_validations = ['user_ratio', 'match_checking']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update_category()
            self.response_status = status.HTTP_201_CREATED
        return self

    def _update_category(self) -> Categories:
        self.category.title = self.cleaned_data['title']
        self.category.save()
        return self.category

    @property
    @lru_cache()
    def category(self) -> Union[Categories, None]:
        try:
            return Categories.objects.get(id=self.cleaned_data['id'])
        except Categories.DoesNotExist:
            return None

    @property
    @lru_cache()
    def categories(self) -> Union[List[Categories], None]:
        return Categories.objects.all()

    def user_ratio(self):
        if not self.cleaned_data['current_user'].is_superuser:
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
            self.response_status = status.HTTP_403_FORBIDDEN

    def match_checking(self):
        if self.categories.filter(title__iexact=self.cleaned_data['title']).exists():
            self.add_error('title', f"Category {self.cleaned_data['title']} already exists")
            self.response_status = status.HTTP_400_BAD_REQUEST
