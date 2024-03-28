from utils.services import ServiceWithResult

from models_app.models.categories.model import Categories

from functools import lru_cache

from typing import Union, List


class CategoriesService(ServiceWithResult):
    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.categories
        return self

    @property
    @lru_cache()
    def categories(self) -> Union[List[Categories], None]:
        return Categories.objects.all()
