from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from drf_yasg.utils import swagger_auto_schema

from models_app.models.photo.model import Photo
from core_api.serializers.photo.photo import PhotoSerializer
from core_api.services.photo.show import PhotoService
from core_api.services.photo.update import UpdatePhotoService
from core_api.services.photo.delete import PhotoDeleteService
from core_api.serializers.photo.create_photo import CreatePhotoSerializer
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from core_api.scheme.photo import photo_show, update_photo, delete_photo

from utils.services import ServiceOutcome


class PhotoView(APIView,
                MultiPartParser):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Photo.objects.all()
    serializer_class = CreatePhotoSerializer

    @swagger_auto_schema(**photo_show)
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(PhotoService, {'id': kwargs['id'], 'current_user': request.user.id})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(PhotoSerializer(outcome.result).data, status=outcome.response_status)

    @swagger_auto_schema(**update_photo)
    def put(self, request, **kwargs):
        outcome = ServiceOutcome(UpdatePhotoService, {'id': kwargs['id'], 'current_user': request.user} |
                                 request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CreatePhotoSerializer(outcome.result).data, status=outcome.response_status)

    @swagger_auto_schema(**delete_photo)
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(PhotoDeleteService, {'id': kwargs['id'], 'current_user': request.user})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(outcome.result, status=outcome.response_status)
