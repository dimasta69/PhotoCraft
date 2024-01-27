from django import forms
from django.core.exceptions import ObjectDoesNotExist

from models_app.models.photo.model import Photo

from utils.services import ServiceWithResult

from functools import lru_cache


class PhotoService(ServiceWithResult):
    id = forms.IntegerField(required=True)

    custom_validations = ['photo_presence']

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self._show()
        return self

    def _show(self):
        return self.get_photo

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
