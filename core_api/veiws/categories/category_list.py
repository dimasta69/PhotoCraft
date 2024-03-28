from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from models_app.models.categories.model import Categories
from core_api.serializers.categories.categories_list import CategoriesSerializer
from core_api.services.categories.show_list import CategoriesService
from core_api.services.categories.create import CategoryCreateServcie
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from utils.services import ServiceOutcome
from core_api.scheme.categories import categories_list, create_category


class CategoriesView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    @swagger_auto_schema(**categories_list)
    def get(self, request):
        outcome = ServiceOutcome(CategoriesService, request.data)
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CategoriesSerializer(outcome.result, many=True).data, status=outcome.response_status)

    @swagger_auto_schema(**create_category)
    def post(self, request):
        outcome = ServiceOutcome(CategoryCreateServcie, {'current_user': request.user} | request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CategoriesSerializer(outcome.result).data, status=outcome.response_status)

