from drf_yasg import openapi

from core_api.serializers.categories.categories_list import CategoriesSerializer

categories_list = {
    'operation_description': 'Get categories list',
    'tags': ['core-api/categories'],
    'responses': {200: openapi.Response('Success', CategoriesSerializer)}
}

create_category = {
    'operation_description': 'Create category',
    'tags': ['core-api/categories'],
    'request_body': openapi.Schema(
        title='core_api_photo_create_schema',
        description='Create photo schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(type=openapi.TYPE_INTEGER),
            title=openapi.Schema(type=openapi.TYPE_STRING),
        ),
        required=['id', 'title']
    ),
    'responses': {201: openapi.Response('Success', CategoriesSerializer)}
}

category_show = {
    'operation_description': 'Get category',
    'tags': ['core-api/category'],
    'responses': {200: openapi.Response(
        'Success', CategoriesSerializer)}
}

update_category = {
    'operation_description': 'Update category',
    'tags': ['core-api/category'],
    'request_body': openapi.Schema(
        title='core_api_category_update_schema',
        description='Update category schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(type=openapi.TYPE_INTEGER),
            title=openapi.Schema(type=openapi.TYPE_STRING),
        ),
        required=['id', 'title']),
    'responses': {201: openapi.Response('Success', CategoriesSerializer)}
}

delete_category = {
    'operation_description': 'Delete category',
    'tags': ['core-api/category']
}
