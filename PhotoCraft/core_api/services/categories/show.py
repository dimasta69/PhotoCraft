from django.core.exceptions import ObjectDoesNotExist
from django import forms
from rest_framework import status

from utils.services import ServiceWithResult

from functools import lru_cache

from models_app.models.categories.model import Categories


class CategoryService(ServiceWithResult):
    id = forms.IntegerField(required=True)

    custom_validations = ['category_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.category
        return self

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
                                                        f"{self.cleaned_data['id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND
