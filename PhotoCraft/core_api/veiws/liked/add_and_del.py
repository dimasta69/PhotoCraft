from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from core_api.services.liked.add_and_del import LikedService
from core_api.serializers.liked.liked import LikedSerializer
from models_app.models.liked.model import Liked


class LikedView(APIView):
    queryset = Liked.objects.all()
    serializer_class = LikedSerializer

    @permission_classes([IsAuthenticated])
    def post(self, request):
        outcome = LikedService(dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(LikedSerializer(outcome.process()).data, status.HTTP_201_CREATED)
