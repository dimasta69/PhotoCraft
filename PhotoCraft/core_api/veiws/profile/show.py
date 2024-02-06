from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from models_app.models.users.model import User
from core_api.serializers.profile.serializer import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = ProfileSerializer

    def get(self, request):
        return Response(ProfileSerializer(request.user).data)
