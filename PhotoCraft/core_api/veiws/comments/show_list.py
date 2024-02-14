from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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

    @swagger_auto_schema(operation_description='Get comments', tags=['core-api/comments'],
                         responses={
                             '200': openapi.Response(
                                 description='Success',
                                 examples={
                                     "application/json": {
                                         "pagination": {
                                             "current_page": 0,
                                             "per_page": 0,
                                             "next_page": None,
                                             "prev_page": None,
                                             "total_pages": 0,
                                             "total_count": 0
                                         },
                                         "results": [
                                             {
                                                 "id": 0,
                                                 "user_id": 0,
                                                 "photo_id": 1,
                                                 "reply_id": "null",
                                                 "text": "string",
                                                 "publicated_at": "date",
                                                 "updated_ad": "date"
                                             },
                                         ]
                                     }
                                 }
                             )
                         },
                         manual_parameters=[
                             openapi.Parameter(name="page",
                                               in_=openapi.IN_QUERY,
                                               description='Page number',
                                               type=openapi.TYPE_INTEGER),
                             openapi.Parameter(name='per_page',
                                               in_=openapi.IN_QUERY,
                                               description='Page size',
                                               type=openapi.TYPE_INTEGER),
                             openapi.Parameter(name='photo_id',
                                               in_=openapi.IN_QUERY,
                                               description='Filter by user',
                                               type=openapi.TYPE_INTEGER,
                                               required=True)])
    def get(self, request):
        outcome = ServiceOutcome(CommentsListService, dict(request.GET.items()))
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(
            {'pagination': CustomPagination(outcome.result, current_page=outcome.service.cleaned_data['page'],
                                            per_page=outcome.service.cleaned_data['per_page']).to_json(),
             'results': CommentsSerializer(outcome.result.object_list, many=True).data})

    @swagger_auto_schema(operation_description='Update post', tags=['core-api/comments'],
                         request_body=openapi.Schema(
                             title='core_api_photo_update_schema',
                             description='Update photo schema',
                             type=openapi.TYPE_OBJECT,
                             properties=dict(
                                 photo_id=openapi.Schema(type=openapi.TYPE_INTEGER),
                                 text=openapi.Schema(type=openapi.TYPE_STRING),
                                 reply_id=openapi.Schema(type=openapi.TYPE_INTEGER),
                             ),
                             required=['photo_id', 'text']
                         ),
                         responses={201: openapi.Response('Success', CommentsSerializer)})
    def post(self, request):
        outcome = ServiceOutcome(CommentCreateService, {'current_user': request.user} | request.data.dict())
        if bool(outcome.errors):
            return Response(outcome.errors, status.HTTP_400_BAD_REQUEST)
        return Response(CommentsSerializer(outcome.result).data, status.HTTP_201_CREATED)


