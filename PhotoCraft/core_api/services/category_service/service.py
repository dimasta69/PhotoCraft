from service_objects.services import Service

from django import forms

from models_app.models.Categories.model import Categories


class CategoryService(Service):
    def process(self):
        return Categories.objects.all()
