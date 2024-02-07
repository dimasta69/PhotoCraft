from django.core.paginator import Paginator, EmptyPage
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from functools import lru_cache

from photo_craft.settings.restframework import *

from models_app.models.photo.model import Photo
from models_app.models.categories.model import Categories
from models_app.models.users.model import User

from utils.services import ServiceWithResult


class PhotoListService(ServiceWithResult):
    page = forms.IntegerField(required=False)
    per_page = forms.IntegerField(required=False)
    category_id = forms.IntegerField(required=False)
    order_by = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)
    current_user = forms.IntegerField(required=False)
    status = forms.CharField(required=False)

    custom_validations = ['category_presence', 'order_presence', 'user_presence', 'status_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photo()
        return self

    def _get_photo(self):
        per_page = self.cleaned_data['per_page']
        page = self.cleaned_data['page']

        try:
            return Paginator(self._checking_user_affiliation, per_page=(per_page or REST_FRAMEWORK['PAGE_SIZE'])).page(
                page or 1)
        except EmptyPage:
            return Paginator(self._checking_user_affiliation,
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
    def user(self):
        try:
            return User.objects.get(id=self.cleaned_data['user_id'])
        except User.DoesNotExist:
            return None

    @property
    @lru_cache()
    def photo(self):
        return Photo.objects.all()

    @property
    def _filter_by_category(self):
        if self.cleaned_data.get('category_id'):
            return self.photo.filter(category=self.category)
        return self.photo

    @property
    def _photo_by_ordering(self):
        if self.cleaned_data.get('order_by'):
            return self._filter_by_category.order_by(self.cleaned_data['order_by'])
        return self._filter_by_category

    @property
    def _filter_by_user(self):
        if self.cleaned_data.get('user_id'):
            return self._photo_by_ordering.filter(user_id=self.user)
        return self._photo_by_ordering

    @property
    def _checking_user_affiliation(self):
        if (self.cleaned_data.get('user_id') == self.cleaned_data.get('current_user') and
                self.cleaned_data.get('current_user') is not None):
            if self.cleaned_data['status']:
                return self._filter_by_user.filter(status=self.cleaned_data['status'])
            return self._filter_by_user
        return self._filter_by_user.filter(status='Published')

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))

    def order_presence(self):
        if self.cleaned_data.get('order_by'):
            if not self.cleaned_data.get('order_by') in ['id', 'category_id', 'user_id', 'publicated_at', 'updated_at']:
                self.add_error('order_by', ObjectDoesNotExist(f"Field in model with "
                                                              f"{self.cleaned_data['order_by']} not found"))

    def user_presence(self):
        if self.cleaned_data.get('user_id'):
            if not self.user:
                self.add_error('user_id', ObjectDoesNotExist(f"User with id="
                                                             f"{self.cleaned_data['user_id']} not found"))

    def current_user_presence(self):
        if self.cleaned_data.get('current_user'):
            if not self.user:
                self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                                  f"{self.cleaned_data['current_user']} not found"))

    def status_presence(self):
        if self.cleaned_data['status']:
            if not self.cleaned_data['status'] in Photo.STATUS_CHOICES:
                self.add_error('status', ObjectDoesNotExist("Status with"
                                                            f"{self.cleaned_data['status']} not found"))
