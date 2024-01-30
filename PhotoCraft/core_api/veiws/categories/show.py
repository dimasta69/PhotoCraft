from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.categories.model import Categories
from core_api.serializers.categories.categories_list import CategoriesSerializer
from core_api.services.categories.show import CategoryService
from core_api.services.categories.delete import CategoryDeleteServcie
from core_api.services.categories.update import CategoryUpdateServcie
from core_api.permissions import IsAuthenticatedAndIsPostRequest

from utils.services import ServiceOutcome


class CategoryView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def get(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategoriesSerializer(outcome.result).data)

    def put(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryUpdateServcie, {'id': kwargs['id'], 'current_user': request.user} |
                                 request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategoriesSerializer(outcome.result).data, status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryDeleteServcie,
                                 {'id': kwargs['id'], 'current_user': request.user})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Object deleted successfully.'}, status.HTTP_200_OK)
