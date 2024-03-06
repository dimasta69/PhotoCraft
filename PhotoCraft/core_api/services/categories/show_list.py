from utils.services import ServiceWithResult

from models_app.models.categories.model import Categories

from functools import lru_cache


class CategoriesService(ServiceWithResult):
    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.categories
        return self

    @property
    @lru_cache()
    def categories(self):
        try:
            return Categories.objects.all()
        except Categories.DoesNotExist:
            return 0

