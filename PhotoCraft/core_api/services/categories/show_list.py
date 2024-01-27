from utils.services import ServiceWithResult

from models_app.models.categories.model import Categories

from functools import lru_cache


class CategoriesService(ServiceWithResult):
    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.category
        return self

    @property
    @lru_cache()
    def category(self):
        return Categories.objects.all()

