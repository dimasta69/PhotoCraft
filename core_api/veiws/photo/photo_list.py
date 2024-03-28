from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from core_api.permissions import IsAuthenticatedAndIsPostRequest

from drf_yasg.utils import swagger_auto_schema

from models_app.models.photo.model import Photo
from core_api.serializers.photo.photo_list import PhotoListSerializer
from core_api.serializers.photo.photo import PhotoSerializer
from core_api.services.photo.show_list import PhotoListService
from core_api.serializers.photo.create_photo import CreatePhotoSerializer
from core_api.services.photo.create import CreatePhotoService
from core_api.scheme.photo import photo_list_show, create_photo

from utils.pagination import CustomPagination
from utils.services import ServiceOutcome


class PhotoListView(APIView,
                    MultiPartParser):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Photo.objects.all()
    serializer_class = CreatePhotoSerializer

    @swagger_auto_schema(**photo_list_show)
    def get(self, request):
        outcome = ServiceOutcome(PhotoListService, {'current_user': request.user.id} | dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(
            {'pagination': CustomPagination(outcome.result, current_page=outcome.service.cleaned_data['page'],
                                            per_page=outcome.service.cleaned_data['per_page']).to_json(),
             'results': PhotoListSerializer(outcome.result.object_list, many=True).data})

    @swagger_auto_schema(**create_photo)
    def post(self, request):
        outcome = ServiceOutcome(CreatePhotoService, {'current_user': request.user} | request.data.dict(),
                                 request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(PhotoSerializer(outcome.result).data, status=outcome.response_status)
