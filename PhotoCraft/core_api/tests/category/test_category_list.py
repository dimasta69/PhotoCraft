from django.test import TestCase

from models_app.factories.users import UserFactory
from models_app.factories.photo import PhotoFactory
from models_app.factories.category import CategoryFactory


class ListCreateCategoryViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user_1 = UserFactory.create(create_token=True, set_superuser=True)
        cls.user_2 = UserFactory.create(create_token=True)
        cls.category_1 = CategoryFactory(title='abcd')
        cls.category_2 = CategoryFactory()
        cls.photo_1 = PhotoFactory.create_batch(3, user_id=cls.user_1, status='Moderation',
                                                category_id=cls.category_1)
        cls.photo_1 = PhotoFactory.create_batch(1, user_id=cls.user_1, status='Moderation',
                                                category_id=cls.category_2)
        cls.photo_2 = PhotoFactory.create_batch(5, user_id=cls.user_1, status='Published',
                                                category_id=cls.category_2)

    def test_view_return_200_if_api_token_not_passed(self):
        resp = self.client.get('/core_api/categories/',
                               content_type='application/json')
        self.assertEqual(resp.status_code, 200)

    def test_create_return_201_is_superuser(self):
        resp = self.client.post('/core_api/categories/',
                                {
                                    'title': 'dada'
                                },
                                HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 201)

    def test_create_return_403_not_superuser(self):
        resp = self.client.post('/core_api/categories/',
                                {
                                    'title': 'dada'
                                },
                                HTTP_AUTHORIZATION=f'Token {self.user_2.auth_token}')
        self.assertEqual(resp.status_code, 403)

    def test_create_return_404_already_exists(self):
        resp = self.client.post('/core_api/categories/',
                                {
                                    'title': 'ABCD'
                                },
                                HTTP_AUTHORIZATION=f'Token {self.user_1.auth_token}')
        self.assertEqual(resp.status_code, 404)
