from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from models_app.models.photo.model import Photo
from core_api.serializers.photo.photo.serializer import PhotoSerializer
from core_api.services.photo.get_photo.service import PhotoService
from core_api.services.photo.create.service import CreatePhotoService


class PhotoView(APIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get(self, request, **kwargs):
        outcome = PhotoService({'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoService(outcome.process()).data)

    @permission_classes([IsAuthenticated])
    def put(self, request, **kwargs):
        outcome = CreatePhotoService({'id': kwargs['id']} | request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.process()).data, status.HTTP_200_OK)

