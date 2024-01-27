from django.core.paginator import Paginator, EmptyPage
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from functools import lru_cache

from photo_craft.settings.restframework import *

from models_app.models.photo.model import Photo
from models_app.models.categories.model import Categories

from utils.services import ServiceWithResult


class PhotoListService(ServiceWithResult):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    category_id = forms.IntegerField(required=False)
    order_by = forms.CharField(required=False)

    custom_validations = ['category_presence', 'order_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._photo()
        return self

    def _photo(self):
        per_page = self.cleaned_data['per_page']
        page = self.cleaned_data['page']

        try:
            return Paginator(self.photo_by_ordering, per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(
                page or 1)
        except EmptyPage:
            return Paginator(self.photo_by_ordering.none(),
                             per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(1)

    @property
    @lru_cache()
    def category(self):
        try:
            return Categories.objects.get(id=self.cleaned_data['category_id'])
        except Categories.DoesNotExist:
            return None

    @property
    @lru_cache()
    def photo(self):
        return Photo.objects.all()

    @property
    def filter_by_category(self):
        if self.cleaned_data.get('category_id'):
            return self.photo.filter(category=self.category)
        return self.photo

    @property
    def photo_by_ordering(self):
        if self.cleaned_data.get('order_by'):
            return self.filter_by_category.order_by(self.cleaned_data['order_by'])
        return self.filter_by_category

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))

    def order_presence(self):
        if self.cleaned_data.get('order_by'):
            if not hasattr(Photo, self.cleaned_data.get('order_by')):
                self.add_error('order_by', ObjectDoesNotExist(f"Field in model with "
                                                              f"{self.cleaned_data['order_by']} not found"))
