import json

from django.test import TestCase

from django.test.client import encode_multipart

from rest_framework.test import APIClient

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory


class CategoryDeleteUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory.create(create_token=True, set_superuser=True)
        cls.user_2 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory(title='abcd')
        cls.category_2 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create_batch(3, user=cls.user_1, status='Moderation',
                                                category=cls.category_1)
        cls.photo_1 = PhotoFactory.create_batch(1, user=cls.user_1, status='Moderation',
                                                category=cls.category_2)
        cls.photo_2 = PhotoFactory.create_batch(5, user=cls.user_1, status='Published',
                                                category=cls.category_2)

    def test_view_return_200(self):
        resp = self.client.get(f'/core_api/category/{self.category_1.id}/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_view_return_404_invalid_id(self):
        resp = self.client.get(f'/core_api/category/99/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_update_return_200_parameters_superuser(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'title': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/category/{self.category_2.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 201)

    def test_update_return_403_parameters_not_superuser(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'title': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/category/{self.category_2.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_update_return_404_already_exists(self):
        resp = self.client.post('/core_api/category/{self.category_2.id}/',
                                {
                                    'title': 'ABCD'
                                },
                                HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 404)

    def test_delete_return_204_superuser(self):
        resp = self.client.delete(f'/core_api/category/{self.category_1.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 204)

    def test_delete_return_403_not_superuser(self):
        resp = self.client.delete(f'/core_api/category/{self.category_1.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_count(self):
        resp = self.client.get(f'/core_api/category/{self.category_1.id}/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

        resp_json = json.loads(resp.content)
        self.assertTrue(resp_json['count'] == 3)

        resp_2 = self.client.get(f'/core_api/category/{self.category_2.id}/',
                                 content_type='application/json')
        self.assertEqual(resp_2.status_code, 200)

        resp_json_2 = json.loads(resp_2.content)
        self.assertTrue(resp_json_2['count'] == 6)
