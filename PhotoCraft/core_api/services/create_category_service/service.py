from service_objects.services import Service

from django import forms

from models_app.models.Categories.model import Categories


class CreateCategoryService(Service):
    title = forms.CharField(required=True)

    def process(self):
        if self.is_valid():
            return Categories.objects.create(title=self.cleaned_data['title'])
        return self
