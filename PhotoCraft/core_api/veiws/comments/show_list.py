from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


from models_app.models.comments.model import Comments
from core_api.serializers.comments.comments import CommentsSerializer
from core_api.services.comments.show_list import CommentsListService
from core_api.services.comments.create import CommentCreateService
from core_api.permissions import IsAuthenticatedAndIsPostRequest
from utils.services import ServiceOutcome
from utils.pagination import CustomPagination


class CommentsView(APIView):
    permission_classes = [IsAuthenticatedAndIsPostRequest]
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get(self, request):
        outcome = ServiceOutcome(CommentsListService, dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(
            {'pagination': CustomPagination(outcome.result, current_page=outcome.service.cleaned_data['page'],
                                            per_page=outcome.service.cleaned_data['per_page']).to_json(),
             'results': CommentsSerializer(outcome.result.object_list, many=True).data})

    def post(self, request):
        outcome = ServiceOutcome(CommentCreateService,{'current_user': request.user} | request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CommentsSerializer(outcome.result).data, status.HTTP_201_CREATED)
