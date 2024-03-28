from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from models_app.models.categories.model import Categories
from core_api.serializers.categories.categories_list import CategoriesSerializer
from core_api.serializers.categories.create_category import CreateCategoriesSerializer
from core_api.services.categories.show import CategoryService
from core_api.services.categories.delete import CategoryDeleteServcie
from core_api.services.categories.update import CategoryUpdateServcie
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from core_api.scheme.categories import category_show, update_category, delete_category

from utils.services import ServiceOutcome


class CategoryView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Categories.objects.all()
    serializer_class = CreateCategoriesSerializer

    @swagger_auto_schema(**category_show)
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CategoriesSerializer(outcome.result).data, status=outcome.response_status)

    @swagger_auto_schema(**update_category)
    def put(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryUpdateServcie, {'id': kwargs['id'], 'current_user': request.user} |
                                 request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CategoriesSerializer(outcome.result).data, status=outcome.response_status)

    @swagger_auto_schema(**delete_category)
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryDeleteServcie,
                                 {'id': kwargs['id'], 'current_user': request.user})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response({'message': 'Object deleted successfully.'}, status=outcome.response_status)
