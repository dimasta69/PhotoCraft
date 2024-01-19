from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.categories.model import Categories
from core_api.serializers.categories.serializer import CategoriesSerializer
from core_api.services.categories.service import CategoriesService


class CategoriesView(APIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def get(self, request):
        outcome = CategoriesService()
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CategoriesSerializer(outcome.process(), many=True).data)
