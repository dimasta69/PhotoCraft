from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from models_app.models.users.model import User
from core_api.serializers.profile.serializer import ProfileSerializer

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    @swagger_auto_schema(operation_description='Get profile information', tags=['core-api/profile'],
                         responses={200: openapi.Response(
                             'Success', ProfileSerializer)})
    def get(self, request):
        return Response(ProfileSerializer(request.user).data)
