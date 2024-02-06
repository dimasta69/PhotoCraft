from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from core_api.permissions import IsAuthenticatedAndIsPostRequest

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from models_app.models.photo.model import Photo
from core_api.serializers.photo.photo_list import PhotoListSerializer
from core_api.serializers.photo.photo import PhotoSerializer
from core_api.services.photo.show_list import PhotoListService
from core_api.services.photo.create import CreatePhotoService

from utils.pagination import CustomPagination
from utils.services import ServiceOutcome


class PhotoListView(APIView,
                    MultiPartParser):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    @swagger_auto_schema(operation_description='Get photo list', tags=['core-api/photos'],
                         responses={200: openapi.Response(
                             'Success', PhotoListSerializer)})
    def get(self, request):
        outcome = ServiceOutcome(PhotoListService, {'current_user': request.user} | dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'pagination': CustomPagination(outcome.result, current_page=outcome.service.cleaned_data['page'],
                                                        per_page=outcome.service.cleaned_data['per_page']).to_json(),
                         'results': PhotoListSerializer(outcome.result.object_list, many=True).data})

    @swagger_auto_schema(operation_description='Create post', tags=['core-api/photos'],
                         request_body=openapi.Schema(
                             title='core_api_photo_create_schema',
                             description='Create photo schema',
                             type=openapi.TYPE_OBJECT,
                             properties=dict(
                                 id=openapi.Schema(type=openapi.TYPE_INTEGER),
                                 title=openapi.Schema(type=openapi.TYPE_STRING),
                                 description=openapi.Schema(type=openapi.TYPE_STRING),
                                 photo=openapi.Schema(type=openapi.TYPE_FILE),
                                 category_id=openapi.Schema(type=openapi.TYPE_INTEGER),
                             ),
                             required=['id', 'photo']
                         ),
                         responses={201: openapi.Response('Success', PhotoListSerializer)})
    def post(self, request):
        outcome = ServiceOutcome(CreatePhotoService, {'current_user': request.user} | request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(PhotoSerializer(outcome.result).data, status.HTTP_201_CREATED)
