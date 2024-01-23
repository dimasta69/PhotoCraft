from service_objects.services import Service

from django import forms

from models_app.models.photo.model import Photo
from models_app.models.users.model import Users


class UpdatePhotoService(Service):
    id = forms.IntegerField(required=True)
    title = forms.CharField(required=False)
    description = forms.CharField(required=False)
    user_id = forms.IntegerField(required=True)
    photo = forms.ImageField(required=False)
    category_id = forms.IntegerField(required=False)

    def process(self):
        if self.is_valid():
            return self.update_photo
        return self

    @property
    def update_photo(self):
        self.check_user()
        photo = Photo.objects.get(id=self.cleaned_data['id'])
        photo.title = self.cleaned_data['title']
        photo.description = self.cleaned_data['description']
        photo.get_category_id = self.cleaned_data['category_id']
        if self.cleaned_data['photo']:
            photo.backup_photo = photo.photo
            photo.photo = self.cleaned_data['photo']
        photo.save()
        return photo

    def check_user(self):
        if (Photo.objects.get(id=self.cleaned_data['id']).user_id != self.cleaned_data['user_id'] or
                Users.objects.get(id=Photo.objects.get(id=self.cleaned_data['id']).user_id).is_superuesr):
            raise ValueError("Error: The user does not have permission to update this photo")
