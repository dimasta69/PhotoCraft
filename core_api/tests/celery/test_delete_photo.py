import datetime
import os

from django.test import TestCase, override_settings
from django.utils.timezone import make_aware

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory
from models_app.models.photo.model import Photo
from photo_craft.settings.celery import OBJECT_TIME_DELETE
from core_api.tasks import my_task


@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
class PhotoDeleteUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        deleted_at_1 = make_aware(datetime.datetime.now()) - OBJECT_TIME_DELETE
        deleted_at_2 = make_aware(datetime.datetime.now()) + OBJECT_TIME_DELETE
        cls.user_1 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create(user=cls.user_1, status='Delete', category=cls.category_1,
                                          deleted_at=deleted_at_1)
        cls.photo_2 = PhotoFactory.create(user=cls.user_1, status='Delete', category=cls.category_1,
                                          deleted_at=deleted_at_2)

    def test_my_task(self):
        self.assertTrue(len(Photo.objects.all()) == 2)
        result = my_task.delay()

        self.assertEqual(result.status, "SUCCESS")
        self.assertFalse(Photo.objects.filter(id=self.photo_1.id).exists())
        self.assertTrue(len(Photo.objects.all()) == 1)
        self.assertFalse(os.path.isfile(self.photo_1.photo.path))
