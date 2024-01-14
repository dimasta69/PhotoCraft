from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from models_app.models.Photo.model import Photo
from core_api.serializers.photo_list_serializer.serializer import PhotoListSerializer
from core_api.serializers.photo_serializer.serializer import PhotoSerializer
from core_api.services.photo_list_service.service import PhotoListService
from core_api.services.create_photo_service.service import CreatePhotoService

from utils.pagination import CustomPagination


class PhotoListView(APIView,
                    MultiPartParser):
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer

    def get(self, request):
        outcome = PhotoListService(dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'pagination': CustomPagination(outcome.process(), current_page=outcome.cleaned_data['page'],
                                                        per_page=outcome.cleaned_data['per_page']).to_json(),
                         'results': PhotoListSerializer(outcome.process().object_list, many=True).data},)

    @permission_classes([IsAuthenticated])
    def post(self, request):
        outcome = CreatePhotoService(request.data, request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.process()).data, status.HTTP_201_CREATED)
