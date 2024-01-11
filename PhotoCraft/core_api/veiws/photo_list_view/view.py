from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.Photo.model import Photo
from core_api.serializers.photo_list_serializer.serializer import PhotoListSerializer
from core_api.services.photo_list_service.service import PhotoListService

from utils.pagination import CustomPagination


class PhotoListView(APIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoListSerializer

    def get(self, request):
        outcome = PhotoListService(dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'pagination': CustomPagination(outcome.process(), current_page=outcome.cleaned_data['page'],
                                                        per_page=outcome.cleaned_data['per_page']).to_json(),
                         'results': PhotoListSerializer(outcome.process().object_list, many=True).data})
