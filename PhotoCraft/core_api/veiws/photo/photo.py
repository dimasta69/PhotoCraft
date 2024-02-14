from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from models_app.models.photo.model import Photo
from core_api.serializers.photo.photo import PhotoSerializer
from core_api.services.photo.show import PhotoService
from core_api.services.photo.update import UpdatePhotoService
from core_api.services.photo.delete import PhotoDeleteService
from core_api.permissions import IsAuthenticatedAndIsPostRequest

from utils.services import ServiceOutcome


class PhotoView(APIView,
                MultiPartParser):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    @swagger_auto_schema(operation_description='Get photo', tags=['core-api/photo'],
                         responses={200: openapi.Response(
                             'Success', PhotoSerializer)})
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(PhotoService, {'id': kwargs['id'], 'current_user': request.user.id})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.result).data)

    @swagger_auto_schema(operation_description='Update post', tags=['core-api/photo'],
                         request_body=openapi.Schema(
                             title='core_api_photo_update_schema',
                             description='Update photo schema',
                             type=openapi.TYPE_OBJECT,
                             properties=dict(
                                 title=openapi.Schema(type=openapi.TYPE_STRING),
                                 photo=openapi.Schema(type=openapi.TYPE_FILE),
                                 category_id=openapi.Schema(type=openapi.TYPE_INTEGER),
                             ),
                         ),
                         responses={201: openapi.Response('Success', PhotoSerializer)})
    def put(self, request, **kwargs):
        outcome = ServiceOutcome(UpdatePhotoService, {'id': kwargs['id'], 'current_user': request.user} |
                                 request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.result).data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description='Delete post',
                         tags=['core-api/photo'])
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(PhotoDeleteService, {'id': kwargs['id'], 'current_user': request.user})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(outcome.result, status.HTTP_204_NO_CONTENT)
