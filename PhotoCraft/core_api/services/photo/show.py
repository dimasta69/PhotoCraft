from service_objects.services import Service

from django import forms

from models_app.models.photo.model import Photo


class PhotoService(Service):
    id = forms.IntegerField(required=True)

    def process(self):
        if self.is_valid():
            return Photo.objects.get(id=self.cleaned_data['id'])
        return self
