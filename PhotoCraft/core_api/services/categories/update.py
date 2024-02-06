from functools import lru_cache

from django.core.exceptions import ObjectDoesNotExist
from django import forms

from service_objects.fields import ModelField

from utils.services import ServiceWithResult

from models_app.models.users.model import User
from models_app.models.categories.model import Categories


class CategoryUpdateServcie(ServiceWithResult):
    id = forms.IntegerField(required=True)
    title = forms.CharField(required=True)
    current_user = ModelField(User)

    custom_validations = ['user_ratio', 'match_checking']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._update()
        return self

    def _update(self):
        category = self.category
        category.title = self.cleaned_data['title']
        category.save()
        return category

    @property
    @lru_cache()
    def category(self):
        try:
            return Categories.objects.get(id=self.cleaned_data['id'])
        except Categories.DoesNotExist:
            return None

    @property
    @lru_cache()
    def categories(self):
        try:
            return Categories.objects.all()
        except Categories.DoesNotExist:
            return None

    def user_ratio(self):
        if not self.cleaned_data['current_user'].is_superuser:
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))

    def match_checking(self):
        if self.categories.filter(title__iexact=self.cleaned_data['title']).exists():
            self.add_error('title', f"Category {self.cleaned_data['title']} already exists")
