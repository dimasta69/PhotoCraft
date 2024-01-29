from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.comments.model import Comments
from core_api.serializers.comments.comments import CommentsSerializer
from core_api.services.comments.show import CommentService
from core_api.services.comments.create import CommentCreateService
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from utils.services import ServiceOutcome
from utils.pagination import CustomPagination


class CommentView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get(self, request, **kwargs):
        outcome = ServiceOutcome(CommentService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CommentsSerializer(outcome.result).data, status.HTTP_200_OK)
