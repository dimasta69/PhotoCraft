from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser

from models_app.models.photo.model import Photo
from core_api.serializers.photo.photo import PhotoSerializer
from core_api.services.photo.show import PhotoService
from core_api.services.photo.update import UpdatePhotoService
from core_api.permissions import IsAuthenticatedAndIsPostRequest

from utils.services import ServiceOutcome


class PhotoView(APIView,
                MultiPartParser):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get(self, requesst, **kwargs):
        outcome = ServiceOutcome(PhotoService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.result).data)

    def put(self, request, **kwargs):
        outcome = ServiceOutcome(UpdatePhotoService, {'id': kwargs['id'], 'current_user': request.user} |
                                 request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.result).data, status.HTTP_200_OK)

