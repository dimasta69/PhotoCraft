import json

from django.test import TestCase
from django.test.client import encode_multipart

from rest_framework.test import APIClient

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory

from photo_craft.settings.restframework import REST_FRAMEWORK

class PhotoDeleteUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory.create(create_token=True)
        cls.user_2 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory()
        cls.category_2 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create(user_id=cls.user_1, status='Moderation',
                                          category_id=cls.category_1)
        cls.photo_2 = PhotoFactory.create(user_id=cls.user_2, status='Published',
                                          category_id=cls.category_2)

    def test_view_return_200_not_auth_token_status_published(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_2.id}/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_view_return_200_auth_token_status_moderation(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 200)

    def test_update_return_200_minimum_parameters(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'title': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/photo/{self.photo_1.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 200)