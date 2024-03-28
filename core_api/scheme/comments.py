from drf_yasg import openapi

from core_api.serializers.comments.comments import CommentsSerializer

comment_show = {
    'operation_description': 'Get comment',
    'tags': ['core-api/comment'],
    'responses': {200: openapi.Response(
        'Success', CommentsSerializer)}
}

update_comment_show = {
    'operation_description': 'Update comment',
    'tags': ['core-api/comment'],
    'request_body': openapi.Schema(
        title='core_api_comment_update_schema',
        description='Comment schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            id=openapi.Schema(type=openapi.TYPE_INTEGER),
            text=openapi.Schema(type=openapi.TYPE_STRING)
        ),
        required=['id', 'text']
    ),
    'responses': {201: openapi.Response('Success', CommentsSerializer)}
}

delete_comment = {
    'operation_description': 'Delete comment',
    'tags': ['core-api/comment']
}

comment_show_list = {
    'operation_description': 'Get comments',
    'tags': ['core-api/comments'],
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
                            "user": {
                                "id": 1,
                                "is_superuser": "bool",
                                "username": "name"
                            },
                            "photo": {'id': 0,
                                      },
                            "reply": "null",
                            "text": "string",
                            "publicated_at": "date",
                            "updated_ad": "date"
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
        openapi.Parameter(name='photo_id',
                          in_=openapi.IN_QUERY,
                          description='Filter by user',
                          type=openapi.TYPE_INTEGER,
                          required=True)]
}

create_comment = {
    'operation_description': 'Update post',
    'tags': ['core-api/comments'],
    'request_body': openapi.Schema(
        title='core_api_photo_update_schema',
        description='Update photo schema',
        type=openapi.TYPE_OBJECT,
        properties=dict(
            photo_id=openapi.Schema(type=openapi.TYPE_INTEGER),
            text=openapi.Schema(type=openapi.TYPE_STRING),
            reply_id=openapi.Schema(type=openapi.TYPE_INTEGER),
        ),
        required=['photo_id', 'text']
    ),
    'responses': {201: openapi.Response('Success', CommentsSerializer)}
}
