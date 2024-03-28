from djoser.views import UserViewSet
from drf_yasg.utils import swagger_auto_schema


class UserViewSet(UserViewSet):
    @swagger_auto_schema(tags=['core-api/auth'])
    def create(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

    @swagger_auto_schema(tags=['core-api/auth'])
    def activate(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)