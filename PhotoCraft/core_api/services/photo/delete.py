from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models.photo.model import Photo
from models_app.models.users.model import User

from functools import lru_cache

from utils.services import ServiceWithResult
from utils.task import schedule_photo_deletion
from service_objects.fields import ModelField


class PhotoDeleteService(ServiceWithResult):
    id = forms.IntegerField(required=True)
    current_user = ModelField(User)

    custom_validations = ['photo_presence', 'user_ratio']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._status()
        return self

    def _status(self):
        if self.get_photo.status in ('Moderation', 'Reject'):
            self.get_photo.delete()
            return {'message': 'Object deleted successfully.'}
        elif self.get_photo.status == 'Delete':
            return {'message': f'The object will be deleted in {self.get_photo.deleted_at}'}
        elif self.get_photo.status == 'Published':
            task = schedule_photo_deletion(self.get_photo.id)
            self.scheduled_deletion_task_id = task.id
            return {'message': f'The object will be deleted in {self.get_photo.deleted_at}'}

    @property
    @lru_cache()
    def get_photo(self):
        try:
            return Photo.objects.get(id=self.cleaned_data['id'])
        except Photo.DoesNotExist:
            return None

    def photo_presence(self):
        if self.cleaned_data['id']:
            if not self.get_photo:
                self.add_error('photo_id', ObjectDoesNotExist(f"Photo with id="
                                                              f"{self.cleaned_data['id']} not found"))

    def user_ratio(self):
        if not ((self.get_photo.user_id.id == self.cleaned_data['current_user'].id) or
                self.cleaned_data['current_user'].is_superuser):
            self.add_error('current_user', ObjectDoesNotExist(f"User with id="
                                                              f"{self.cleaned_data['current_user']} is not the author "
                                                              f"of the post"))
