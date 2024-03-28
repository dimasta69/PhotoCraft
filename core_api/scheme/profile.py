from drf_yasg import openapi

from core_api.serializers.profile.serializer import ProfileSerializer

profile_show = {
    'operation_description': 'Get profile information',
    'tags': ['core-api/profile'],
    'responses': {200: openapi.Response(
        'Success', ProfileSerializer)}
}
