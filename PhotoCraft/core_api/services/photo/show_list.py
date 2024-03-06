from django.core.paginator import Paginator, EmptyPage
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from functools import lru_cache

from rest_framework import status

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
    status = forms.ChoiceField(choices=Photo.STATUS_CHOICES, required=False)

    custom_validations = ['category_presence', 'order_presence', 'user_presence', 'status_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._get_photos()
        return self

    def _get_photos(self):
        try:
            return Paginator(self.get_photos_filtered_ordering, per_page=(self.cleaned_data['per_page'] or
                                                                         REST_FRAMEWORK['PAGE_SIZE'])).page(
                self.cleaned_data['page'] or 1)
        except EmptyPage:
            return Paginator(self.get_photos_filtered_ordering,
                             per_page=(self.cleaned_data['per_page'] or REST_FRAMEWORK['PAGE_SIZE'])).page(1)

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
    def photos(self):
        return Photo.objects.all()

    @property
    def get_photos_filtered_ordering(self):
        photos = self.photos
        if self.cleaned_data.get('category_id'):
            photos = photos.filter(category_id=self.category)
        if self.cleaned_data.get('order_by'):
            photos = photos.order_by(self.cleaned_data['order_by'])
        if self.cleaned_data.get('user_id'):
            photos = photos.filter(user_id=self.user)
        if (self.cleaned_data.get('user_id') == self.cleaned_data.get('current_user') and
                self.cleaned_data.get('current_user') is not None):
            if self.cleaned_data['status']:
                photos = photos.filter(status=self.cleaned_data['status'])
        else:
            photos = photos.filter(status='Published')
        return photos

    def category_presence(self):
        if self.cleaned_data['category_id']:
            if not self.category:
                self.add_error('category_id', ObjectDoesNotExist(f"Category with id="
                                                                 f"{self.cleaned_data['category_id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def order_presence(self):
        if self.cleaned_data.get('order_by'):
            if not self.cleaned_data.get('order_by') in ['id', 'category_id', 'user_id', 'publicated_at', 'updated_at']:
                self.add_error('order_by', ObjectDoesNotExist(f"Field in model with "
                                                              f"{self.cleaned_data['order_by']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def user_presence(self):
        if self.cleaned_data.get('user_id'):
            if not self.user:
                self.add_error('user_id', ObjectDoesNotExist(f"User with id="
                                                             f"{self.cleaned_data['user_id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def current_user_presence(self):
        if self.cleaned_data.get('current_user'):
            if not self.user:
                self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                                  f"{self.cleaned_data['current_user']} not found"))
                self.response_status = status.HTTP_403_FORBIDDEN

    def status_presence(self):
        if self.cleaned_data['status']:
            if not self.cleaned_data['status'] in [choice[0] for choice in Photo.STATUS_CHOICES]:
                self.add_error('status', ObjectDoesNotExist("Status with"
                                                            f"{self.cleaned_data['status']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND
