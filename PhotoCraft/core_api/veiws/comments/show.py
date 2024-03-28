from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

from models_app.models.comments.model import Comments
from core_api.serializers.comments.comments import CommentsSerializer
from core_api.services.comments.show import CommentService
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from core_api.services.comments.updated import CommentUpdatedService
from core_api.services.comments.delete import CommentDeleteService
from core_api.scheme.comments import comment_show, update_comment_show, delete_comment
from utils.services import ServiceOutcome


class CommentView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    @swagger_auto_schema(**comment_show)
    def get(self, request, **kwargs):
        outcome = ServiceOutcome(CommentService, {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CommentsSerializer(outcome.result).data, status=outcome.response_status)

    @swagger_auto_schema(**update_comment_show)
    def put(self, request, **kwargs):
        outcome = ServiceOutcome(CommentUpdatedService,  {'current_user': request.user} | {'id': kwargs['id']} |
                                 request.data.dict())
        if bool(outcome.errors):
            print(123)
            return Response(outcome.errors, status=outcome.response_status)
        return Response(CommentsSerializer(outcome.result).data, status=outcome.response_status)

    @swagger_auto_schema(**delete_comment)
    def delete(self, request, **kwargs):
        outcome = ServiceOutcome(CommentDeleteService, {'current_user': request.user} | {'id': kwargs['id']})
        if bool(outcome.errors):
            return Response(outcome.errors, status=outcome.response_status)
        return Response({'message': 'Object deleted successfully.'}, status=outcome.response_status)


