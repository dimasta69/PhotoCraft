from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from models_app.models.photo.model import Photo
from core_api.serializers.photo.personal_area import PersonalAreaSerializer
from core_api.services.photo.show_personal_area import PersonalAreaService

from utils.pagination import CustomPagination
from utils.services import ServiceOutcome


class PersonalAreaView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = Photo.objects.all()
    serializer_class = PersonalAreaSerializer

    def get(self, request):
        outcome = ServiceOutcome(PersonalAreaService, {'current_user': request.user} | dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'pagination': CustomPagination(outcome.result, current_page=outcome.service.cleaned_data['page'],
                                                        per_page=outcome.service.cleaned_data['per_page']).to_json(),
                         'results': PersonalAreaSerializer(outcome.result.object_list, many=True).data})
