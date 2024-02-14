import json

from django.test import TestCase
from django.test.client import encode_multipart

from rest_framework.test import APIClient

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory

from photo_craft.settings.restframework import REST_FRAMEWORK


class ListCreatePhotoViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory.create(create_token=True)
        cls.user_2 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory()
        cls.category_2 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create_batch(3, user_id=cls.user_1, status='Moderation',
                                                category_id=cls.category_1)
        cls.photo_1 = PhotoFactory.create_batch(1, user_id=cls.user_1, status='Moderation',
                                                category_id=cls.category_2)
        cls.photo_2 = PhotoFactory.create_batch(5, user_id=cls.user_1, status='Published',
                                                category_id=cls.category_2)

    def test_view_return_200_if_api_token_not_passed(self):
        resp = self.client.get('/core_api/photos/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_filter_status(self):
        resp = self.client.get('/core_api/photos/',
                               {'page': 1, 'per_page': 100, 'current_user': self.user_1.id, 'user_id': self.user_1.id},
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertTrue(len(resp_json['results']) == 9)

    def test_pagination_is_two(self):
        resp = self.client.get('/core_api/photos/',
                               {'page': 2, 'per_page': 2},
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertTrue('pagination' in resp_json)
        self.assertTrue('results' in resp_json)
        self.assertTrue(resp_json['pagination']['current_page'] == 2)
        self.assertTrue(resp_json['pagination']['per_page'] == 2)
        self.assertTrue(resp_json['pagination']['next_page'] == 3)
        self.assertTrue(resp_json['pagination']['prev_page'] == 1)
        self.assertTrue(resp_json['pagination']['total_pages'] == 3)
        self.assertTrue(len(resp_json['results']) == REST_FRAMEWORK['PAGE_SIZE'])

    def test_view_maximum_parameters(self):
        resp = self.client.get('/core_api/photos/',
                               {'page': 1, 'per_page': 100, 'current_user': self.user_1.id, 'user_id': self.user_1.id, 'category_id':
                                   self.category_1.id, 'order_by': 'id', 'status': 'Moderation'},
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertTrue(len(resp_json['results']) == 3)

    def test_view_create_return_401_auth_token_false(self):
        with open('./core_api/tests/pixel.jpg', 'rb') as image:
            params = {'id': 51,
                      'title': 'title',
                      'photo': image}

            resp = self.client.post('/core_api/photos/',
                                    params,
                                    format='multipart')
            self.assertEqual(resp.status_code, 403)

    def test_view_create_return_201_minimum_parameters_auth_token_true(self):
        with open('./core_api/tests/pixel.jpg', 'rb') as image:
            params = {'id': 55,
                      'title': 'title',
                      'photo': image}

            resp = self.client.post('/core_api/photos/',
                                    params,
                                    format='multipart',
                                    HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')

            self.assertEqual(resp.status_code, 201)

    def test_view_create_return_201_maximum_parameters(self):
        with open('./core_api/tests/pixel.jpg', 'rb') as image:
            params = {'id': 77,
                      'title': 'title',
                      'photo': image,
                      'description': 'dadsadasdasdada asdadsa',
                      'category_id': self.category_1.id}

            resp = self.client.post('/core_api/photos/',
                                    params,
                                    format='multipart',
                                    HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
            self.assertEqual(resp.status_code, 201)


#


