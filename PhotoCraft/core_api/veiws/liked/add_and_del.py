from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from core_api.permissions import IsAuthenticatedAndIsPostRequest
from core_api.services.liked.add_and_del import LikedService
from core_api.serializers.liked.create_like import CreateLikedSerializer
from core_api.serializers.liked.liked import LikedSerializer
from core_api.scheme.liked import liked_create
from models_app.models.liked.model import Liked
from utils.services import ServiceOutcome


class LikedView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Liked.objects.all()
    serializer_class = CreateLikedSerializer

    @swagger_auto_schema(**liked_create)
    def post(self, request):
        outcome = ServiceOutcome(LikedService, {'current_user': request.user} | request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(LikedSerializer(outcome.result).data, status=outcome.response_status)
