import json
import os

from django.test import TestCase
from django.test.client import encode_multipart

from rest_framework.test import APIClient

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory
from models_app.factories.like import LikeFactory
from models_app.factories.comment import CommentFactory

from photo_craft.settings.restframework import REST_FRAMEWORK


class PhotoDeleteUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory.create(create_token=True)
        cls.user_2 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory()
        cls.category_2 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create(user=cls.user_1, status='Moderation',
                                          category=cls.category_1)
        cls.photo_2 = PhotoFactory.create(user=cls.user_2, status='Published',
                                          category=cls.category_2)
        cls.like_1 = LikeFactory.create(user=cls.user_1, photo=cls.photo_1)
        cls.comment_1 = CommentFactory.create(photo=cls.photo_1, user=cls.user_1, reply=None)

    def test_view_return_200_not_auth_token_status_published(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_2.id}/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_view_return_404_invalid_id(self):
        resp = self.client.get(f'/core_api/photo/99/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_view_return_404_not_auth_token_status_moderation(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_view_return_200_auth_token_status_moderation(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 200)

    def test_view_return_404_auth_token_status_moderation(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 404)

    def test_update_return_200_minimum_parameters_auth_token_valid(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'title': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/photo/{self.photo_1.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 201)

    def test_update_return_403_auth_token_invalid(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'title': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/photo/{self.photo_1.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_update_return_200_maximum_parameters(self):
        with open('./core_api/tests/photo/pixel.jpg', 'rb') as image:
            factory = APIClient()
            params = {
                'title': 'adada',
                'description': 'asdadas',
                'photo': image,
                'category_id': self.category_2.id,
            }
            content = encode_multipart('BoUnDaRyStRiNg', params)
            content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
            resp = factory.put(f'/core_api/photo/{self.photo_1.id}/',
                               content,
                               content_type=content_type,
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
            self.assertEqual(resp.status_code, 201)
            resp_json = json.loads(resp.content)
            self.assertTrue(resp_json['status'] == 'Moderation')

    def test_update_return_404_invalid_category(self):
        with open('./core_api/tests/photo/pixel.jpg', 'rb') as image:
            factory = APIClient()
            params = {
                'title': 'adada',
                'description': 'asdadas',
                'photo': image,
                'category_id': 99,
            }
            content = encode_multipart('BoUnDaRyStRiNg', params)
            content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
            resp = factory.put(f'/core_api/photo/{self.photo_1.id}/',
                               content,
                               content_type=content_type,
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
            self.assertEqual(resp.status_code, 404)

    def test_delete_return_204_token_valid(self):
        resp = self.client.delete(f'/core_api/photo/{self.photo_2.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 204)

    def test_delete_return_403_token_invalid(self):
        resp = self.client.delete(f'/core_api/photo/{self.photo_1.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_delete_return_403_token_false(self):
        resp = self.client.delete(f'/core_api/photo/{self.photo_2.id}/',
                                  content_type='application/json')
        self.assertEqual(resp.status_code, 401)

    def test_count_liked(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        resp_json = json.loads(resp.content)
        self.assertTrue(resp_json['number_of_likes'] == 1)

    def test_liked_post(self):
        resp_like = self.client.post(f'/core_api/like/',
                                     {
                                         'photo_id': self.photo_2.id,
                                     },
                                     HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')

        resp = self.client.get(f'/core_api/photo/{self.photo_2.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        resp_json = json.loads(resp.content)
        self.assertTrue(resp_json['number_of_likes'] == 1)

    def test_liked_delete(self):
        resp_like = self.client.post(f'/core_api/like/',
                                     {
                                         'photo_id': self.photo_1.id,
                                     },
                                     HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')

        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        resp_json = json.loads(resp.content)
        self.assertTrue(resp_json['number_of_likes'] == 0)

    def test_count_comments(self):
        resp = self.client.get(f'/core_api/photo/{self.photo_1.id}/',
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        resp_json = json.loads(resp.content)
        self.assertTrue(resp_json['number_of_comments'] == 1)
