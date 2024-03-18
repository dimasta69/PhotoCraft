import json

from django.test import TestCase

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory
from models_app.factories.comment import CommentFactory


class ListCreateCommentViewTest(TestCase):
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

    def test_view_return_200_if_api_token_not_passed(self):
        resp = self.client.get('/core_api/comments/',
                               {
                                   'photo_id': self.photo_1.id
                               },
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_pagination_status(self):
        resp = self.client.get('/core_api/comments/',
                               {'page': 1, 'per_page': 100, 'photo_id': self.photo_1.id},
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        resp_json = json.loads(resp.content)
        self.assertTrue(len(resp_json['results']) == 2)

    def test_view_create_return_201_minimum_parameters_auth_token_true(self):
        resp = self.client.post('/core_api/comments/',
                                {
                                    'photo_id': self.photo_2.id,
                                    'text': 'text',
                                },
                                HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')

        self.assertEqual(resp.status_code, 201)

    def test_view_create_return_403_minimum_parameters_auth_token_false(self):
        resp = self.client.post('/core_api/comments/',
                                {
                                    'photo_id': self.photo_2.id,
                                    'text': 'text',
                                })

        self.assertEqual(resp.status_code, 401)

    def test_view_create_return_201_maximum_parameters_auth_token_true(self):
        resp = self.client.post('/core_api/comments/',
                                {
                                    'photo_id': self.photo_2.id,
                                    'text': 'text',
                                    'reply_id': self.comment_1.id,
                                },
                                HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')

        self.assertEqual(resp.status_code, 201)
