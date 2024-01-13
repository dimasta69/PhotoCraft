from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.Categories.model import Categories
from core_api.serializers.category_serializer.serializer import CategorySerializer
from core_api.services.category_service.service import CategoryService
from core_api.services.create_category_service.service import CreateCategoryService


class CategoryView(APIView):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def get(self, request):
        outcome = CategoryService()
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategorySerializer(outcome.process(), many=True).data)

    def post(self, request):
        outcome = CreateCategoryService(dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategorySerializer(CreateCategoryService.process()).data, status.HTTP_201_CREATED)

