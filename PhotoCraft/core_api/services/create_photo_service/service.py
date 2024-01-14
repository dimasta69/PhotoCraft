from service_objects.services import Service

from django import forms

from models_app.models.Photo.model import Photo
from models_app.models.Users.model import Users
from models_app.models.Categories.model import Categories


class CreatePhotoService(Service):
    title = forms.CharField(required=True)
    description = forms.CharField(required=False)
    user_id = forms.IntegerField(required=False)
    photo = forms.ImageField(required=True)
    category_id = forms.IntegerField(required=False)

    def process(self):
        if self.is_valid():
            user_id = Users.objects.get(id=self.cleaned_data['user_id']).id
            category_id = Categories.objects.get(id=self.cleaned_data['category_id']).id
            return Photo.objects.create(title=self.cleaned_data['title'],
                                        description=self.cleaned_data['description'],
                                        user_id=user_id,
                                        photo=self.cleaned_data['photo'],
                                        category_id=category_id)
        return self
