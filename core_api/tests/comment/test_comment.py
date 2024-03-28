import json

from django.test import TestCase
from django.test.client import encode_multipart

from rest_framework.test import APIClient

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory
from models_app.factories.comment import CommentFactory


class CommentDeleteUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory.create(create_token=True)
        cls.user_2 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create(user=cls.user_1, status='Moderation',
                                          category=cls.category_1)
        cls.photo_2 = PhotoFactory.create(user=cls.user_2, status='Moderation',
                                          category=cls.category_1)

        cls.comment_1 = CommentFactory.create(photo=cls.photo_1, user=cls.user_1)
        cls.comment_2 = CommentFactory.create(photo=cls.photo_1, user=cls.user_2, reply=cls.comment_1)
        cls.comment_3 = CommentFactory.create(photo=cls.photo_1, user=cls.user_2)

    def test_view_return_200_not_auth_token_status_published(self):
        resp = self.client.get(f'/core_api/comment/{self.comment_1.id}/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_view_return_404_invalid_id(self):
        resp = self.client.get(f'/core_api/comment/99/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 404)

    def test_update_return_200_parameters_auth_token_valid(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'text': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/comment/{self.comment_1.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 201)

    def test_update_return_403_auth_token_invalid(self):
        factory = APIClient()
        content = encode_multipart('BoUnDaRyStRiNg', {'text': 'adsasda'})
        content_type = 'multipart/form-data; boundary=BoUnDaRyStRiNg'
        resp = factory.put(f'/core_api/comment/{self.comment_1.id}/',
                           content,
                           content_type=content_type,
                           HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_delete_return_204_token_valid(self):
        resp = self.client.delete(f'/core_api/comment/{self.comment_3.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 204)

    def test_delete_return_403_token_invalid(self):
        resp = self.client.delete(f'/core_api/comment/{self.comment_3.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_delete_return_403_token_false(self):
        resp = self.client.delete(f'/core_api/comment/{self.comment_3.id}/',
                                  content_type='application/json')
        self.assertEqual(resp.status_code, 401)

    def test_delete_reply(self):
        resp = self.client.delete(f'/core_api/comment/{self.comment_1.id}/',
                                  content_type='application/json',
                                  HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 204)

        resp_list = self.client.get('/core_api/comments/',
                                    {'photo_id': self.photo_1.id},
                                    content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp_list.status_code, 200)
        resp_json = json.loads(resp_list.content)
        self.assertTrue(len(resp_json['results']) == 1)
