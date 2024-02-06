from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from core_api.permissions import IsAuthenticatedAndIsPostRequest
from core_api.services.liked.add_and_del import LikedService
from core_api.serializers.liked.liked import LikedSerializer
from models_app.models.liked.model import Liked
from utils.services import ServiceOutcome


class LikedView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Liked.objects.all()
    serializer_class = LikedSerializer

    @swagger_auto_schema(operation_description='Like the post', tags=['core-api/like'],
                         request_body=openapi.Schema(
                             title='core_api_like_schema',
                             description='Like schema',
                             type=openapi.TYPE_OBJECT,
                             properties=dict(
                                 photo_id=openapi.Schema(type=openapi.TYPE_INTEGER),
                             ),
                             required=['photo_id']
                         ),
                         responses={201: openapi.Response('Success', LikedSerializer)})
    def post(self, request):
        outcome = ServiceOutcome(LikedService, {'current_user': request.user} | request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(LikedSerializer(outcome.result).data, status.HTTP_201_CREATED)
