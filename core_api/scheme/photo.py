from drf_yasg import openapi

from core_api.serializers.photo.photo import PhotoSerializer
from core_api.serializers.photo.photo_list import PhotoListSerializer

photo_show = {
    'operation_description': 'Get photo', 'tags': ['core-api/photo'],
    'responses': {200: openapi.Response(
        'Success', PhotoSerializer)}
}

update_photo = {
    'operation_description': 'Update post', 'tags': ['core-api/photo'],
    'request_body': openapi.Schema(
        title='core_api_photo_update_schema',
        description='Update photo schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            title=openapi.Schema(type=openapi.TYPE_STRING),
            photo=openapi.Schema(type=openapi.TYPE_FILE),
            category_id=openapi.Schema(type=openapi.TYPE_INTEGER),
        ),
    ),
    'responses': {201: openapi.Response('Success', PhotoSerializer)}
}

delete_photo = {
    'operation_description': 'Delete post',
    'tags': ['core-api/photo']
}

photo_list_show = {
    'operation_description': 'Get photo list',
    'tags': ['core-api/photos'],
    'responses': {
        '200': openapi.Response(
            description='Success',
            examples={
                "application/json": {
                    "pagination": {
                        "current_page": 0,
                        "per_page": 0,
                        "next_page": None,
                        "prev_page": None,
                        "total_pages": 0,
                        "total_count": 0
                    },
                    "results": [
                        {
                            "id": 0,
                            "category": 'null',
                            "user": {
                                "id": 0,
                                "is_superuser": 'bool',
                                "username": "name"
                            },
                            "title": "string",
                            "photo_space": "string",
                            "status": "string",
                            "number_of_likes": 0,
                            "number_of_comments": 0
                        },
                    ]
                }
            }
        )
    },
    'manual_parameters': [
        openapi.Parameter(name="page",
                          in_=openapi.IN_QUERY,
                          description='Page number',
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter(name='per_page',
                          in_=openapi.IN_QUERY,
                          description='Page size',
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter(name='user_id',
                          in_=openapi.IN_QUERY,
                          description='Filter by user',
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter(name='category_id',
                          in_=openapi.IN_QUERY,
                          description='Filter by category',
                          type=openapi.TYPE_INTEGER),
        openapi.Parameter(name='order_by',
                          in_=openapi.IN_QUERY,
                          description='Order photo by columns',
                          type=openapi.TYPE_STRING,
                          enum=['id', 'category_id', 'user_id', 'publicated_at', 'updated_at']),
        openapi.Parameter(name='status',
                          in_=openapi.IN_QUERY,
                          description='Filter by status',
                          type=openapi.TYPE_STRING)]
}

create_photo = {
    'operation_description': 'Create post',
    'tags': ['core-api/photos'],
    'request_body': openapi.Schema(
        title='core_api_photo_create_schema',
        description='Create photo schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(type=openapi.TYPE_INTEGER),
            title=openapi.Schema(type=openapi.TYPE_STRING),
            description=openapi.Schema(type=openapi.TYPE_STRING),
            photo=openapi.Schema(type=openapi.TYPE_FILE),
            category_id=openapi.Schema(type=openapi.TYPE_INTEGER),
        ),
        required=['id', 'photo']
    ),
    'responses': {201: openapi.Response('Success', PhotoListSerializer)}
}
