import factory
from factory.django import DjangoModelFactory

from models_app.models.categories.model import Categories


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Categories

    title = factory.Faker('sentence', nb_words=3)
