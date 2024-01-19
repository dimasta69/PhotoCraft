from service_objects.services import Service

from models_app.models.categories.model import Categories


class CategoriesService(Service):
    def process(self):
        return Categories.objects.all()
