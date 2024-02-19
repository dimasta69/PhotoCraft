from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(operation_description='Get category', tags=['core-api/category'],
                         responses={200: openapi.Response(
                             'Success', CategoriesSerializer)})
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CategoriesSerializer(outcome.result).data)

    @swagger_auto_schema(operation_description='Update category', tags=['core-api/category'],
                         request_body=openapi.Schema(
                             title='core_api_category_update_schema',
                             description='Update category schema',
                             type=openapi.TYPE_OBJECT,
                             properties=dict(
                                 id=openapi.Schema(type=openapi.TYPE_INTEGER),
                                 title=openapi.Schema(type=openapi.TYPE_STRING),
                             ),
                             required=['id', 'title']
                         ),
                         responses={201: openapi.Response('Success', CategoriesSerializer)})
    def put(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryUpdateServcie, {'id': kwargs['id'], 'current_user': request.user} |
                                 request.data.dict(), request.FILES)
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CategoriesSerializer(outcome.result).data, status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_description='Delete category',
                         tags=['core-api/category'])
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(CategoryDeleteServcie,
                                 {'id': kwargs['id'], 'current_user': request.user})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response({'message': 'Object deleted successfully.'}, status.HTTP_204_NO_CONTENT)
