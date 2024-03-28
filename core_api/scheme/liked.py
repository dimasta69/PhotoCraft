from drf_yasg import openapi

from core_api.serializers.liked.liked import LikedSerializer

liked_create = {
    'operation_description': 'Like the post',
    'tags': ['core-api/like'],
    'request_body': openapi.Schema(
        title='core_api_like_schema',
        description='Like schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            photo_id=openapi.Schema(type=openapi.TYPE_INTEGER),
        ),
        required=['photo_id']
    ),
    'responses': {201: openapi.Response('Success', LikedSerializer)}
}
