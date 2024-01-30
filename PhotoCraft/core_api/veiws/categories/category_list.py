from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.categories.model import Categories
from core_api.serializers.categories.categories_list import CategoriesSerializer
from core_api.services.categories.show_list import CategoriesService
from core_api.services.categories.create import CategoryCreateServcie
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from utils.services import ServiceOutcome


class CategoriesView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def get(self, request):
        outcome = ServiceOutcome(CategoriesService, request.data)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategoriesSerializer(outcome.result, many=True).data, status.HTTP_200_OK)

    def post(self, request):
        outcome = ServiceOutcome(CategoryCreateServcie, {'current_user': request.user} | request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategoriesSerializer(outcome.result).data, status.HTTP_201_CREATED)

