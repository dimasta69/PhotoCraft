from service_objects.services import Service

from django.core.paginator import Paginator, EmptyPage
from django import forms

from photo_craft.settings.restframework import *

from models_app.models.photo.model import Photo
from models_app.models.categories.model import Categories


class PhotoListService(Service):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    category_id = forms.IntegerField(required=False)
    order_by = forms.CharField(required=False)

    def process(self):
        if self.is_valid():
            per_page = self.cleaned_data['per_page']
            page = self.cleaned_data['page']

            try:
                return Paginator(self._photo_by_ordering, per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(
                    page or 1)
            except EmptyPage:
                return Paginator(self._photo_by_ordering.none(),
                                 per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(1)

    @property
    def _filter_by_category(self):
        if self.cleaned_data['category_id']:
            category = Categories.objects.get(id=self.cleaned_data['category_id'])
            return Photo.objects.filter(category_id=category)
        return Photo.objects.all()

    @property
    def _photo_by_ordering(self):
        if self.cleaned_data['order_by']:
            return self._filter_by_category.order_by(self.cleaned_data['order_by'])
        return self._filter_by_category
