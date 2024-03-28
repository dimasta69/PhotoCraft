import json
import os

from django import forms
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from models_app.models.photo.model import Photo
from models_app.models.users.model import User

from functools import lru_cache

from utils.services import ServiceWithResult
from service_objects.fields import ModelField
from photo_craft.settings.celery import OBJECT_TIME_DELETE

from typing import Union


class PhotoDeleteService(ServiceWithResult):
    id = forms.IntegerField(required=True)
    current_user = ModelField(User)

    custom_validations = ['photo_presence', 'user_ratio']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._delete_obj()
            self.response_status = status.HTTP_204_NO_CONTENT
        return self

    def _delete_obj(self) -> json:
        if self.photo.status in ('Moderation', 'Reject'):
            if self.photo.photo:
                if os.path.isfile(self.photo.photo.path):
                    os.remove(self.photo.photo.path)
            if self.photo.backup_photo:
                if os.path.isfile(self.photo.backup_photo.path):
                    os.remove(self.photo.backup_photo.path)
            self.photo.delete()
            return {'message': 'Object deleted successfully.'}
        elif self.photo.status == 'Delete':
            return {'message': f'Еhe object will be deleted in {self.photo.deleted_at + OBJECT_TIME_DELETE}'}
        elif self.photo.status == 'Published':
            self.photo.set_schedule_deletion()
            return {'message': f'Еhe object will be deleted in {self.photo.deleted_at + OBJECT_TIME_DELETE}'}

    @property
    @lru_cache()
    def photo(self) -> Union[Photo, None]:
        try:
            return Photo.objects.get(id=self.cleaned_data['id'])
        except Photo.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['id']:
            if not self.photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))
                self.response_status = status.HTTP_404_NOT_FOUND

    def user_ratio(self):
        if not ((self.photo.user.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
            self.response_status = status.HTTP_403_FORBIDDEN

