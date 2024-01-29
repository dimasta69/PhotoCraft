from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from models_app.models.comments.model import Comments
from core_api.serializers.comments.comments import CommentsSerializer
from core_api.services.comments.show import CommentService
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from core_api.services.comments.updated import CommentUpdatedService
from core_api.services.comments.delete import CommentDeleteService
from utils.services import ServiceOutcome


class CommentView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get(self, request, **kwargs):
        outcome = ServiceOutcome(CommentService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CommentsSerializer(outcome.result).data, status.HTTP_200_OK)

    def put(self, request, **kwargs):
        outcome = ServiceOutcome(CommentUpdatedService,  {'current_user': request.user} | {'id': kwargs['id']} |
                                 request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CommentsSerializer(outcome.result).data, status.HTTP_200_OK)

    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(CommentDeleteService, {'current_user': request.user} | {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Object deleted successfully.'}, status.HTTP_200_OK)


